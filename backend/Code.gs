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
  NOTIFY: ['ctajung47@gmail.com'],                            // 알림 받을 메일 (박경준·한사라 추가)
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
    if (!d.name || !d.arc || !d.phone) throw new Error('필수값 누락');

    const ss = SpreadsheetApp.openById(CONFIG.SHEET_ID);
    const sh = ss.getSheetByName(CONFIG.SHEET_TAB);
    const now = new Date();
    const ymd = Utilities.formatDate(now, CONFIG.TZ, 'yyMMdd');
    const todayCount = sh.getLastRow() > 1
      ? sh.getRange(2, 1, sh.getLastRow() - 1, 1).getValues().filter(r => String(r[0]).indexOf('WT-' + ymd) === 0).length
      : 0;
    const no = 'WT-' + ymd + '-' + String(todayCount + 1).padStart(3, '0');

    // 1) 폴더 + 파일
    const root = DriveApp.getFolderById(CONFIG.INTAKE_FOLDER_ID);
    const folder = root.createFolder(no + '_' + d.name.replace(/[\\/:*?"<>|]/g, ' ').trim());
    const files = d.files || [];
    const counters = {};
    files.forEach(f => {
      const prefix = ROLE_LABEL[f.role] || '90_기타';
      counters[f.role] = (counters[f.role] || 0) + 1;
      const ext = (f.name.match(/\.[A-Za-z0-9]+$/) || [''])[0];
      const base = f.name.replace(/\.[A-Za-z0-9]+$/, '').slice(0, 60);
      const fname = prefix + (counters[f.role] > 1 ? '-' + counters[f.role] : '') + '_' + base + ext;
      const blob = Utilities.newBlob(Utilities.base64Decode(f.data), f.type || 'application/octet-stream', fname);
      folder.createFile(blob);
    });
    // 접수 원본 JSON (파일 데이터 제외) 보관
    const meta = Object.assign({}, d, { files: files.map(f => ({ role: f.role, name: f.name, type: f.type })) });
    folder.createFile(Utilities.newBlob(JSON.stringify(meta, null, 2), 'application/json', '00_접수정보.json'));

    // 2) 시트 행
    const row = [
      no, Utilities.formatDate(now, CONFIG.TZ, 'yyyy-MM-dd HH:mm'), d.name, d.arc, d.arcOld || '', d.phone, d.visa || '', d.addr || '',
      d.hireDate || '', d.companies || '', d.prev + (d.prevYears ? '(' + d.prevYears + ')' : ''), d.bank || '', d.acct || '',
      d.htId || '', d.htPw || '', files.length, folder.getUrl(), d.proxy || '본인', d.memo || '', '접수', ''
    ];
    sh.appendRow(row);

    // 3) 알림
    const roleCount = {};
    files.forEach(f => { roleCount[f.role] = (roleCount[f.role] || 0) + 1; });
    const body = [
      '새 접수: ' + no,
      '성명: ' + d.name, '외국인등록번호: ' + d.arc, '연락처: ' + d.phone, '최초취업일: ' + (d.hireDate || '-'),
      '근무회사: ' + (d.companies || '-'), '이전환급: ' + d.prev, '계좌: ' + (d.bank || '') + ' ' + (d.acct || ''),
      '입력자: ' + (d.proxy || '본인'), '첨부: ' + files.length + '건 ' + JSON.stringify(roleCount),
      '폴더: ' + folder.getUrl(), '대장: ' + ss.getUrl()
    ].join('\n');
    if (CONFIG.NOTIFY.length) MailApp.sendEmail(CONFIG.NOTIFY.join(','), '[외국인경정 접수] ' + no + ' ' + d.name, body);

    return ContentService.createTextOutput(JSON.stringify({ ok: true, no: no, folderUrl: folder.getUrl() }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ ok: false, error: String(err) }))
      .setMimeType(ContentService.MimeType.JSON);
  } finally {
    lock.releaseLock();
  }
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
