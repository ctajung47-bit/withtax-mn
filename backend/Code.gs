/**
 * 위드택스 외국인 경정청구 — 접수 백엔드 (Google Apps Script)
 * 역할: apply.html 에서 보낸 JSON을 받아
 *   1) 드라이브 접수 폴더에 {접수번호}_{성명} 폴더 생성 + 파일 저장
 *   2) 관리대장 시트 '접수' 탭에 행 추가
 *   3) 담당자 메일 알림
 * 응답: {ok:true, no:'WT-261001-001', folderUrl:'...'}
 */
const CONFIG = {
  INTAKE_FOLDER_ID: '1seSu4MONZJ0NPlPbwDN0Nz-6_oTcbDdj',      // 외국인경정/접수
  SHEET_ID: '1bYZ5BI0jb_2XoYfTe3I5G9cXXrlHQE4xepgAVN2xGIA',  // 관리대장
  SHEET_TAB: '접수',
  NOTIFY: ['ctajung47@gmail.com', 'with02@withtax2020.com'],  // 알림 받을 메일
  TZ: 'Asia/Seoul'
};

const ROLE_LABEL = {
  id_front: '01_신분증앞', id_back: '02_신분증뒤', id_old: '03_변경전등록증',
  simplified: '10_간소화자료', withholding: '20_원천징수영수증', other: '90_기타'
};

function doGet() {
  return ContentService.createTextOutput(JSON.stringify({ ok: true, service: 'withtax-mn intake' }))
    .setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(30000);
  try {
    const d = JSON.parse(e.postData.contents);
    const action = d.action || 'single';
    let out;
    if (action === 'create') out = createIntake(d);
    else if (action === 'file') out = addFile(d);
    else if (action === 'done') out = finishIntake(d);
    else out = singleIntake(d);
    return json(out);
  } catch (err) {
    return json({ ok: false, error: String(err) });
  } finally {
    lock.releaseLock();
  }
}
function json(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
function safeName(s) { return String(s || '').replace(/[\\/:*?"<>|]/g, ' ').trim(); }
function nextNo(sh, now) {
  const ymd = Utilities.formatDate(now, CONFIG.TZ, 'yyMMdd');
  const todayCount = sh.getLastRow() > 1
    ? sh.getRange(2, 1, sh.getLastRow() - 1, 1).getValues().filter(r => String(r[0]).indexOf('WT-' + ymd) === 0).length
    : 0;
  return 'WT-' + ymd + '-' + String(todayCount + 1).padStart(3, '0');
}
function rowFor(no, now, d, fileCount, folderUrl, status) {
  return [
    no, Utilities.formatDate(now, CONFIG.TZ, 'yyyy-MM-dd HH:mm'), d.name, d.arc, d.arcOld || '', d.phone, d.visa || '', d.addr || '',
    d.hireDate || '', d.companies || '', d.prev + (d.prevYears ? '(' + d.prevYears + ')' : ''), d.bank || '', d.acct || '',
    d.htId || '', d.htPw || '', fileCount, folderUrl, d.proxy || '본인', d.memo || '', status, ''
  ];
}
function saveFile(folder, f, idx) {
  const prefix = ROLE_LABEL[f.role] || '90_기타';
  const ext = (f.name.match(/\.[A-Za-z0-9]+$/) || [''])[0];
  const base = f.name.replace(/\.[A-Za-z0-9]+$/, '').slice(0, 60);
  const fname = prefix + (idx > 1 ? '-' + idx : '') + '_' + base + ext;
  folder.createFile(Utilities.newBlob(Utilities.base64Decode(f.data), f.type || 'application/octet-stream', fname));
  return fname;
}
function notify(no, d, files, folder, ss) {
  const roleCount = {};
  files.forEach(f => { roleCount[f.role] = (roleCount[f.role] || 0) + 1; });
  // 알림에는 민감정보(등록번호·계좌·홈택스) 제외 — 상세는 폴더 링크로 확인
  const lines = [
    '📥 새 접수 ' + no,
    '성명: ' + d.name,
    '연락처: ' + d.phone,
    '최초취업일: ' + (d.hireDate || '-'),
    '근무회사: ' + (d.companies || '-'),
    '입력자: ' + (d.proxy || '본인'),
    '첨부: ' + files.length + '건',
    '폴더: ' + folder.getUrl(),
    '대장: ' + ss.getUrl()
  ];
  const body = lines.join('\n');
  // 1) 텔레그램 (토큰·chat id는 스크립트 속성: TG_TOKEN, TG_CHAT_ID)
  try {
    const p = PropertiesService.getScriptProperties();
    const token = p.getProperty('TG_TOKEN'), chat = p.getProperty('TG_CHAT_ID');
    if (token && chat) UrlFetchApp.fetch('https://api.telegram.org/bot' + token + '/sendMessage', {
      method: 'post', contentType: 'application/json', muteHttpExceptions: true,
      payload: JSON.stringify({ chat_id: chat, text: body, disable_web_page_preview: true })
    });
  } catch (e) { console.error('telegram: ' + e); }
  // 2) 이메일
  try {
    if (CONFIG.NOTIFY.length) MailApp.sendEmail(CONFIG.NOTIFY.join(','), '[외국인경정 접수] ' + no + ' ' + d.name, body);
  } catch (e) { console.error('mail: ' + e); }
}

/** 편집기에서 ▶ 실행: 텔레그램 연결 확인 */
function testTelegram() {
  const p = PropertiesService.getScriptProperties();
  const r = UrlFetchApp.fetch('https://api.telegram.org/bot' + p.getProperty('TG_TOKEN') + '/sendMessage', {
    method: 'post', contentType: 'application/json', muteHttpExceptions: true,
    payload: JSON.stringify({ chat_id: p.getProperty('TG_CHAT_ID'), text: '✅ 위드택스 접수 알림 연결 확인' })
  });
  Logger.log(r.getContentText());
}

/** 1단계: 접수 생성 (폴더 + 시트 행 '업로드중') */
function createIntake(d) {
  if (!d.name || !d.arc || !d.phone) throw new Error('필수값 누락');
  const ss = SpreadsheetApp.openById(CONFIG.SHEET_ID), sh = ss.getSheetByName(CONFIG.SHEET_TAB);
  const now = new Date(), no = nextNo(sh, now);
  const folder = DriveApp.getFolderById(CONFIG.INTAKE_FOLDER_ID).createFolder(safeName(d.name) + '_' + no);
  const meta = Object.assign({}, d, { no: no, files: d.fileList || [] });
  folder.createFile(Utilities.newBlob(JSON.stringify(meta, null, 2), 'application/json', '00_접수정보.json'));
  sh.appendRow(rowFor(no, now, d, 0, folder.getUrl(), '업로드중'));
  return { ok: true, no: no, folderId: folder.getId(), folderUrl: folder.getUrl() };
}
/** 2단계: 파일 1개 추가 */
function addFile(d) {
  const folder = DriveApp.getFolderById(d.folderId);
  const fname = saveFile(folder, d.file, d.idx || 1);
  return { ok: true, saved: fname };
}
/** 3단계: 마무리 (시트 상태·첨부수 갱신 + 알림) */
function finishIntake(d) {
  const ss = SpreadsheetApp.openById(CONFIG.SHEET_ID), sh = ss.getSheetByName(CONFIG.SHEET_TAB);
  const folder = DriveApp.getFolderById(d.folderId);
  const vals = sh.getRange(2, 1, Math.max(sh.getLastRow() - 1, 1), 1).getValues();
  for (let i = 0; i < vals.length; i++) if (vals[i][0] === d.no) {
    sh.getRange(i + 2, 16).setValue(d.count || 0);
    sh.getRange(i + 2, 20).setValue('접수');
  }
  notify(d.no, d, d.files || [], folder, ss);
  return { ok: true, no: d.no, folderUrl: folder.getUrl() };
}
/** 구버전: 한 번에 전송 */
function singleIntake(d) {
  if (!d.name || !d.arc || !d.phone) throw new Error('필수값 누락');
  const ss = SpreadsheetApp.openById(CONFIG.SHEET_ID), sh = ss.getSheetByName(CONFIG.SHEET_TAB);
  const now = new Date(), no = nextNo(sh, now);
  const folder = DriveApp.getFolderById(CONFIG.INTAKE_FOLDER_ID).createFolder(safeName(d.name) + '_' + no);
  const files = d.files || []; const counters = {};
  files.forEach(f => { counters[f.role] = (counters[f.role] || 0) + 1; saveFile(folder, f, counters[f.role]); });
  const meta = Object.assign({}, d, { files: files.map(f => ({ role: f.role, name: f.name, type: f.type })) });
  folder.createFile(Utilities.newBlob(JSON.stringify(meta, null, 2), 'application/json', '00_접수정보.json'));
  sh.appendRow(rowFor(no, now, d, files.length, folder.getUrl(), '접수'));
  notify(no, d, files, folder, ss);
  return { ok: true, no: no, folderUrl: folder.getUrl() };
}

/** 편집기에서 ▶ 실행해 권한 승인 + 동작 확인용 */
function selfTest() {
  const fake = { postData: { contents: JSON.stringify({
    name: 'TEST USER', arc: '990101-5000000', phone: '010-0000-0000', visa: 'E-9', addr: '테스트', hireDate: '2019-03-26',
    companies: '테스트회사', prev: 'no', bank: '국민은행', acct: '000000000000', htId: 'TEST', htPw: 'x', memo: 'selfTest', proxy: '',
    files: [{ role: 'other', name: 'hello.txt', type: 'text/plain', data: Utilities.base64Encode('hello') }]
  }) } };
  Logger.log(doPost(fake).getContent());
}
