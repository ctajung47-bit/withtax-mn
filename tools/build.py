# -*- coding: utf-8 -*-
"""withtax-mn 사이트 빌더 — 공통 셸 + 3페이지. 실행: python3 build.py (저장소 루트에 index/calc/apply.html 생성)"""
import os, re
S = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(S, '..')  # 저장소 루트
LOGO = open(S + '/logo.b64').read()
PHOTO = open(S + '/photo.b64').read()
TAXCORE = open(S + '/taxcore.js', encoding='utf-8').read()

def T(mn, ko, cls=''):
    """bilingual span — CSS shows only the active language"""
    return f'<span class="t {cls}"><span class="mn">{mn}</span><span class="ko">{ko}</span></span>'

CSS = r"""
:root{
  --navy:#0F1F3D; --navy-2:#17305C; --gold:#C9A24A; --gold-soft:#F3E9CF;
  --brand:#1B3F8B; --brand-2:#2F8FD6; --brand-soft:#E7EFF6;
  --ground:#FAF9F5; --surface:#FFFFFF;
  --ink:#152238; --ink-2:#44536B; --ink-3:#6F7D93; --line:#E2DFD6;
  --urgent:#B8650E; --urgent-soft:#FDF2E3; --ok:#1E7A4E; --ok-soft:#E4F4EB; --bad:#B4322E; --bad-soft:#FBE9E7;
  --focus:#2F8FD6;
  --f-disp:"Noto Serif KR","IBM Plex Sans",serif;
  --f-body:"IBM Plex Sans","IBM Plex Sans KR","Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){color-scheme:dark;--navy:#0A1529;--navy-2:#122444;--gold:#D8B45E;--gold-soft:#3A3120;--brand:#7FB2F0;--brand-2:#5CB0EC;--brand-soft:#1B2A40;--ground:#0E1622;--surface:#162131;--ink:#E6ECF4;--ink-2:#AEBBCD;--ink-3:#8795AB;--line:#2A384C;--urgent:#F0A850;--urgent-soft:#2E2112;--ok:#5FCB93;--ok-soft:#14291E;--bad:#F28B85;--bad-soft:#36191A}}
:root[data-theme="dark"]{color-scheme:dark;--navy:#0A1529;--navy-2:#122444;--gold:#D8B45E;--gold-soft:#3A3120;--brand:#7FB2F0;--brand-2:#5CB0EC;--brand-soft:#1B2A40;--ground:#0E1622;--surface:#162131;--ink:#E6ECF4;--ink-2:#AEBBCD;--ink-3:#8795AB;--line:#2A384C;--urgent:#F0A850;--urgent-soft:#2E2112;--ok:#5FCB93;--ok-soft:#14291E;--bad:#F28B85;--bad-soft:#36191A}
*{box-sizing:border-box}
[hidden]{display:none!important}
html{scroll-behavior:smooth}
body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--f-body);font-size:16px;line-height:1.6;overflow-x:hidden}
h1,h2,h3{margin:0;line-height:1.3;text-wrap:balance;overflow-wrap:anywhere}
p{margin:0}
img{max-width:100%}
a{color:var(--brand)}
/* 단일 언어 표시 */
.t .mn,.t .ko{display:contents}
html.lang-mn .ko{display:none!important}
html.lang-ko .mn{display:none!important}
.wrap{max-width:1000px;margin:0 auto;padding-inline:20px}
.topbar{background:var(--surface);border-bottom:1px solid var(--line);position:sticky;top:env(safe-area-inset-top,0px);z-index:10}
.topbar .wrap{display:flex;align-items:center;gap:10px;padding-block:10px;flex-wrap:wrap}
.topbar img{height:38px;width:auto;display:block;flex:none}
.nav{display:flex;gap:2px;margin-left:auto;flex-wrap:wrap}
.nav a{font-size:15px;font-weight:600;color:var(--ink-2);text-decoration:none;padding:10px 10px;border-radius:8px;min-height:44px;display:inline-flex;align-items:center}
.nav a:hover,.nav a[aria-current="page"]{background:var(--ground);color:var(--ink)}
.lang{display:inline-flex;border:1px solid var(--line);border-radius:999px;background:var(--ground);padding:3px;gap:2px;flex:none}
.lang button{font:inherit;font-weight:700;font-size:14px;border:0;background:transparent;color:var(--ink-3);padding:8px 14px;border-radius:999px;cursor:pointer;min-height:40px}
.lang button[aria-pressed="true"]{background:var(--navy);color:#fff}
@media (max-width:480px){.topbar .wrap{gap:6px}.nav{width:100%;order:3;margin-left:0;justify-content:space-between}.nav a{padding:8px 6px;font-size:14px;flex:1;justify-content:center}}

.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;font:inherit;font-weight:700;font-size:16px;padding:12px 22px;min-height:48px;border-radius:10px;text-decoration:none;cursor:pointer;border:1px solid transparent;line-height:1.3;text-align:center;overflow-wrap:anywhere}
.btn.gold{background:var(--gold);color:#0F1F3D}
.btn.navy{background:var(--navy);color:#fff}
.btn.ghost{background:transparent;color:var(--ink);border-color:var(--line)}
.btn.ghost.onnavy{color:#fff;border-color:rgba(255,255,255,.4)}
.btn:disabled{opacity:.5;cursor:not-allowed}
.btn.block{width:100%}
.btn:focus-visible,button:focus-visible,a:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible,summary:focus-visible,[tabindex]:focus-visible{outline:3px solid var(--focus);outline-offset:2px}

section.sec{padding-block:44px}
.sec-h{margin-bottom:20px}
.sec-h h2{font-family:var(--f-disp);font-size:26px;font-weight:700}
.sec-h p{margin-top:8px;color:var(--ink-2);font-size:16px;max-width:64ch}
.lead{color:var(--ink-2);font-size:17px;max-width:60ch}
.eyebrow{font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:var(--gold);font-weight:700}
.note{font-size:14px;color:var(--ink-3)}
.callout{background:var(--urgent-soft);border-left:4px solid var(--urgent);border-radius:8px;padding:12px 14px;font-size:15px}
.callout.ok{background:var(--ok-soft);border-left-color:var(--ok)}
.callout.info{background:var(--brand-soft);border-left-color:var(--brand)}

.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
@media (max-width:760px){.grid3{grid-template-columns:1fr}}
@media (max-width:520px){.grid2{grid-template-columns:1fr}}
.item{min-width:0}
.item h3{font-size:18px;margin-bottom:6px}
.item p{color:var(--ink-2);font-size:15.5px}
.num{font-family:var(--f-disp);font-size:26px;font-weight:700;color:var(--gold);line-height:1;margin-bottom:8px}

.field{display:flex;flex-direction:column;gap:6px;min-width:0}
.field>label,.field>.lbl{font-weight:600;font-size:16px}
.req::after{content:" *";color:var(--bad)}
.field input,.field select,.field textarea{font:inherit;font-size:16px;color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:12px 14px;width:100%;min-width:0;min-height:48px}
.field textarea{min-height:88px;resize:vertical}
.hint{font-size:14px;color:var(--ink-3)}
.err{color:var(--bad);font-size:15px;font-weight:600;min-height:1.2em}
.seg{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.seg.three{grid-template-columns:repeat(3,1fr)}
.seg label{border:1px solid var(--line);border-radius:10px;padding:10px 12px;font-size:15.5px;cursor:pointer;display:flex;align-items:flex-start;gap:10px;background:var(--surface);min-width:0;line-height:1.35;min-height:48px}
.seg input{accent-color:var(--brand);margin:3px 0 0;flex:none;width:18px;height:18px;padding:0;border:0;min-height:0}
.seg label .t{flex:1;min-width:0;overflow-wrap:anywhere}
.seg label:has(input:checked){border-color:var(--brand);background:var(--brand-soft);color:var(--brand);font-weight:600}
@media (max-width:420px){.seg.three{grid-template-columns:1fr 1fr}}
.won{position:relative}
.won input{padding-right:40px!important;text-align:right;font-variant-numeric:tabular-nums}
.won span{position:absolute;right:14px;top:50%;transform:translateY(-50%);color:var(--ink-3);font-size:14px;pointer-events:none}

footer{background:var(--surface);border-top:1px solid var(--line);padding-block:28px 44px;font-size:14px;color:var(--ink-3)}
footer .wrap{display:flex;flex-direction:column;gap:6px}
footer b{color:var(--ink-2);font-weight:600}

.page{max-width:760px;margin:0 auto;padding:32px 20px 72px}
.page-h h1{font-family:var(--f-disp);font-size:28px;font-weight:700}
.page-h p{margin-top:8px;color:var(--ink-2)}
.stepbar{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin:22px 0 18px;counter-reset:st}
.stepbar div{counter-increment:st;font-size:14px;color:var(--ink-3);padding-top:10px;border-top:4px solid var(--line);min-width:0;word-break:keep-all;overflow-wrap:break-word}
.stepbar div::before{content:counter(st) ". ";font-weight:700}
.stepbar div.cur{color:var(--navy);border-top-color:var(--gold);font-weight:700}
.stepbar div.done{border-top-color:var(--ok);color:var(--ok)}
.form{display:flex;flex-direction:column;gap:18px}
.form h2{font-size:20px}
.form h3{font-size:16px;color:var(--brand);margin-top:4px}
.form hr{border:0;border-top:1px dashed var(--line);margin:4px 0}
.navrow{display:flex;gap:10px;flex-wrap:wrap;margin-top:8px}
.navrow .btn{flex:1 1 160px}
.slots{display:flex;flex-direction:column;gap:12px}
.slot{border:1px solid var(--line);border-radius:12px;padding:14px;background:var(--surface)}
.slot.ok{border-color:var(--ok)}
.slot.over{border-color:var(--brand);background:var(--brand-soft);border-style:dashed}
.slot-h{display:flex;justify-content:space-between;gap:8px;font-weight:600;font-size:16px;margin-bottom:4px}
.slot-h .t{flex:1;min-width:0}
.slot-sub{font-size:14px;color:var(--ink-3);margin-bottom:10px}
.slot-b{display:flex;flex-wrap:wrap;gap:8px}
label.file{display:inline-flex;align-items:center;gap:6px;border:1px dashed var(--brand-2);color:var(--brand);border-radius:10px;padding:10px 14px;font-size:15px;font-weight:600;cursor:pointer;background:var(--surface);position:relative;min-height:48px}
label.file.cam{border-style:solid;background:var(--brand-soft)}
label.file input{position:absolute;width:1px;height:1px;opacity:0;pointer-events:none}
.dz{font-size:13px;color:var(--ink-3);margin-top:6px}
@media (hover:none){.dz{display:none}}
.flist{list-style:none;margin:8px 0 0;padding:0;display:flex;flex-direction:column;gap:4px}
.flist:empty{display:none}
.flist li{display:flex;align-items:center;gap:8px;font-size:14.5px;background:var(--ground);border-radius:8px;padding:6px 10px;min-width:0}
.flist li img{width:36px;height:36px;object-fit:cover;border-radius:5px;flex:none}
.flist li .pdf{width:36px;height:36px;border-radius:5px;background:var(--bad-soft);color:var(--bad);font-size:11px;font-weight:700;display:grid;place-items:center;flex:none}
.flist li .nm{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.flist li .sz{color:var(--ink-3);font-variant-numeric:tabular-nums;flex:none;font-size:13px}
.flist li button{border:0;background:transparent;color:var(--ink-2);font-size:20px;cursor:pointer;width:40px;height:40px;flex:none;border-radius:8px}
.flist li button:hover{background:var(--bad-soft);color:var(--bad)}
.prog{display:flex;flex-direction:column;gap:8px;font-size:16px;color:var(--ink-2);padding:16px;border-radius:10px;background:var(--brand-soft)}
.prog-h{display:flex;justify-content:space-between;align-items:baseline;gap:12px}
.prog-h b{font-size:22px;color:var(--navy);font-variant-numeric:tabular-nums;flex:none}
.prog .bar{height:14px;border-radius:7px;background:#fff;border:1px solid var(--line);overflow:hidden}
.prog .bar i{display:block;height:100%;width:0;background:var(--navy);transition:width .3s}
.prog-hint{font-size:14px;color:var(--ink-3)}
.summary{display:grid;grid-template-columns:auto 1fr;gap:8px 14px;font-size:15px;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:14px}
.summary dt{color:var(--ink-3)}.summary dd{margin:0;min-width:0;overflow-wrap:anywhere}
.agree{display:flex;gap:12px;align-items:flex-start;font-size:15.5px;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px 14px}
.agree input{width:22px;height:22px;margin-top:2px;accent-color:var(--brand);flex:none}
.agree details{font-size:14px;color:var(--ink-3);margin-top:6px}
.agree summary{cursor:pointer;min-height:28px}
.done{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:26px 20px}
.done .ok{width:52px;height:52px;border-radius:50%;background:var(--ok-soft);color:var(--ok);display:grid;place-items:center;margin:0 auto 10px;font-size:26px;font-weight:700}
.done h2{font-size:21px;text-align:center}
.done p{margin-top:6px;color:var(--ink-2);text-align:center}
.pw{background:var(--urgent-soft);border-radius:12px;padding:14px;display:flex;flex-direction:column;gap:10px}
.pwrow{position:relative}
.pwrow button{position:absolute;right:6px;top:50%;transform:translateY(-50%);font:inherit;font-size:13px;border:0;background:var(--ground);color:var(--ink-2);border-radius:8px;padding:8px 10px;cursor:pointer;min-height:36px}
.proxy{display:flex;gap:12px;align-items:flex-start;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px 14px;font-size:15.5px}
.proxy input{width:22px;height:22px;accent-color:var(--brand);margin-top:2px;flex:none}
.proxy>div{flex:1;min-width:0}
#proxyFields{margin-top:10px}


:root{
  --navy:#0F1F3D; --navy-2:#17305C; --gold:#C9A24A; --gold-soft:#F3E9CF;
  --brand:#1B3F8B; --brand-2:#2F8FD6; --brand-soft:#E7EFF6;
  --ground:#FAF9F5; --surface:#FFFFFF;
  --ink:#152238; --ink-2:#44536B; --ink-3:#6F7D93; --line:#E2DFD6;
  --urgent:#B8650E; --urgent-soft:#FDF2E3; --ok:#1E7A4E; --ok-soft:#E4F4EB; --bad:#B4322E; --bad-soft:#FBE9E7;
  --focus:#2F8FD6;
  --f-disp:"Noto Serif KR","IBM Plex Sans",serif;
  --f-body:"IBM Plex Sans","IBM Plex Sans KR","Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){color-scheme:dark;--navy:#0A1529;--navy-2:#122444;--gold:#D8B45E;--gold-soft:#3A3120;--brand:#7FB2F0;--brand-2:#5CB0EC;--brand-soft:#1B2A40;--ground:#0E1622;--surface:#162131;--ink:#E6ECF4;--ink-2:#AEBBCD;--ink-3:#8795AB;--line:#2A384C;--urgent:#F0A850;--urgent-soft:#2E2112;--ok:#5FCB93;--ok-soft:#14291E;--bad:#F28B85;--bad-soft:#36191A}}
:root[data-theme="dark"]{color-scheme:dark;--navy:#0A1529;--navy-2:#122444;--gold:#D8B45E;--gold-soft:#3A3120;--brand:#7FB2F0;--brand-2:#5CB0EC;--brand-soft:#1B2A40;--ground:#0E1622;--surface:#162131;--ink:#E6ECF4;--ink-2:#AEBBCD;--ink-3:#8795AB;--line:#2A384C;--urgent:#F0A850;--urgent-soft:#2E2112;--ok:#5FCB93;--ok-soft:#14291E;--bad:#F28B85;--bad-soft:#36191A}
*{box-sizing:border-box}
[hidden]{display:none!important}
html{scroll-behavior:smooth}
body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--f-body);font-size:16px;line-height:1.6;overflow-x:hidden}
h1,h2,h3{margin:0;line-height:1.3;text-wrap:balance;overflow-wrap:anywhere}
p{margin:0}
img{max-width:100%}
a{color:var(--brand)}
/* 단일 언어 표시 */
.t .mn,.t .ko{display:contents}
html.lang-mn .ko{display:none!important}
html.lang-ko .mn{display:none!important}
.wrap{max-width:1000px;margin:0 auto;padding-inline:20px}
.topbar{background:var(--surface);border-bottom:1px solid var(--line);position:sticky;top:env(safe-area-inset-top,0px);z-index:10}
.topbar .wrap{display:flex;align-items:center;gap:10px;padding-block:10px;flex-wrap:wrap}
.topbar img{height:38px;width:auto;display:block;flex:none}
.nav{display:flex;gap:2px;margin-left:auto;flex-wrap:wrap}
.nav a{font-size:15px;font-weight:600;color:var(--ink-2);text-decoration:none;padding:10px 10px;border-radius:8px;min-height:44px;display:inline-flex;align-items:center}
.nav a:hover,.nav a[aria-current="page"]{background:var(--ground);color:var(--ink)}
.lang{display:inline-flex;border:1px solid var(--line);border-radius:999px;background:var(--ground);padding:3px;gap:2px;flex:none}
.lang button{font:inherit;font-weight:700;font-size:14px;border:0;background:transparent;color:var(--ink-3);padding:8px 14px;border-radius:999px;cursor:pointer;min-height:40px}
.lang button[aria-pressed="true"]{background:var(--navy);color:#fff}
@media (max-width:480px){.topbar .wrap{gap:6px}.nav{width:100%;order:3;margin-left:0;justify-content:space-between}.nav a{padding:8px 6px;font-size:14px;flex:1;justify-content:center}}

.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;font:inherit;font-weight:700;font-size:16px;padding:12px 22px;min-height:48px;border-radius:10px;text-decoration:none;cursor:pointer;border:1px solid transparent;line-height:1.3;text-align:center;overflow-wrap:anywhere}
.btn.gold{background:var(--gold);color:#0F1F3D}
.btn.navy{background:var(--navy);color:#fff}
.btn.ghost{background:transparent;color:var(--ink);border-color:var(--line)}
.btn.ghost.onnavy{color:#fff;border-color:rgba(255,255,255,.4)}
.btn:disabled{opacity:.5;cursor:not-allowed}
.btn.block{width:100%}
.btn:focus-visible,button:focus-visible,a:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible,summary:focus-visible,[tabindex]:focus-visible{outline:3px solid var(--focus);outline-offset:2px}

section.sec{padding-block:44px}
.sec-h{margin-bottom:20px}
.sec-h h2{font-family:var(--f-disp);font-size:26px;font-weight:700}
.sec-h p{margin-top:8px;color:var(--ink-2);font-size:16px;max-width:64ch}
.lead{color:var(--ink-2);font-size:17px;max-width:60ch}
.eyebrow{font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:var(--gold);font-weight:700}
.note{font-size:14px;color:var(--ink-3)}
.callout{background:var(--urgent-soft);border-left:4px solid var(--urgent);border-radius:8px;padding:12px 14px;font-size:15px}
.callout.ok{background:var(--ok-soft);border-left-color:var(--ok)}
.callout.info{background:var(--brand-soft);border-left-color:var(--brand)}

.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
@media (max-width:760px){.grid3{grid-template-columns:1fr}}
@media (max-width:520px){.grid2{grid-template-columns:1fr}}
.item{min-width:0}
.item h3{font-size:18px;margin-bottom:6px}
.item p{color:var(--ink-2);font-size:15.5px}
.num{font-family:var(--f-disp);font-size:26px;font-weight:700;color:var(--gold);line-height:1;margin-bottom:8px}

.field{display:flex;flex-direction:column;gap:6px;min-width:0}
.field>label,.field>.lbl{font-weight:600;font-size:16px}
.req::after{content:" *";color:var(--bad)}
.field input,.field select,.field textarea{font:inherit;font-size:16px;color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:12px 14px;width:100%;min-width:0;min-height:48px}
.field textarea{min-height:88px;resize:vertical}
.hint{font-size:14px;color:var(--ink-3)}
.err{color:var(--bad);font-size:15px;font-weight:600;min-height:1.2em}
.seg{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.seg.three{grid-template-columns:repeat(3,1fr)}
.seg label{border:1px solid var(--line);border-radius:10px;padding:10px 12px;font-size:15.5px;cursor:pointer;display:flex;align-items:flex-start;gap:10px;background:var(--surface);min-width:0;line-height:1.35;min-height:48px}
.seg input{accent-color:var(--brand);margin:3px 0 0;flex:none;width:18px;height:18px;padding:0;border:0;min-height:0}
.seg label .t{flex:1;min-width:0;overflow-wrap:anywhere}
.seg label:has(input:checked){border-color:var(--brand);background:var(--brand-soft);color:var(--brand);font-weight:600}
@media (max-width:420px){.seg.three{grid-template-columns:1fr 1fr}}
.won{position:relative}
.won input{padding-right:40px!important;text-align:right;font-variant-numeric:tabular-nums}
.won span{position:absolute;right:14px;top:50%;transform:translateY(-50%);color:var(--ink-3);font-size:14px;pointer-events:none}

footer{background:var(--surface);border-top:1px solid var(--line);padding-block:28px 44px;font-size:14px;color:var(--ink-3)}
footer .wrap{display:flex;flex-direction:column;gap:6px}
footer b{color:var(--ink-2);font-weight:600}

.page{max-width:760px;margin:0 auto;padding:32px 20px 72px}
.page-h h1{font-family:var(--f-disp);font-size:28px;font-weight:700}
.page-h p{margin-top:8px;color:var(--ink-2)}
.form{display:flex;flex-direction:column;gap:18px;margin-top:22px}
.paytools{display:flex;flex-wrap:wrap;gap:8px 12px;align-items:center}
.paytools .won{flex:1 1 180px}
.chk{display:inline-flex;align-items:center;gap:8px;font-size:15px;cursor:pointer;min-height:44px}
.chk input{accent-color:var(--brand);width:18px;height:18px;margin:0}
.years{display:grid;grid-template-columns:repeat(5,1fr);gap:6px}
.years .y{display:flex;flex-direction:column;gap:3px;min-width:0}
.years .y small{font-size:13px;color:var(--ink-3);font-weight:600}
.years .y input{padding:8px!important;font-size:15px;text-align:right;min-height:44px}
@media (max-width:460px){.years{grid-template-columns:repeat(3,1fr)}}
.extra{border:1px dashed var(--line);border-radius:12px;padding:12px 14px}
.extra summary{cursor:pointer;font-weight:600;font-size:16px;list-style:none;display:flex;justify-content:space-between;gap:8px;min-height:32px;align-items:center}
.extra summary::-webkit-details-marker{display:none}
.extra summary::after{content:"+";color:var(--ink-3);font-size:22px}
.extra[open] summary::after{content:"−"}
.result{border:1px solid var(--brand-2);border-radius:14px;overflow:hidden;background:var(--surface)}
.rhead{background:var(--navy);color:#fff;padding:14px 16px}
.rhead .big{font-size:28px;font-weight:700;font-variant-numeric:tabular-nums;line-height:1.2}
.rhead .lbl2{font-size:14px;opacity:.85}
.tblwrap{overflow-x:auto}
.rt{width:100%;border-collapse:collapse;font-size:14.5px;font-variant-numeric:tabular-nums}
.rt th,.rt td{padding:8px 10px;text-align:right;border-bottom:1px solid var(--line);white-space:nowrap}
.rt th:first-child,.rt td:first-child{text-align:left}
.rt th{font-weight:600;color:var(--ink-3);font-size:12.5px;background:var(--ground)}
.rt td.g{color:var(--ok);font-weight:700}.rt td.m{color:var(--ink-3)}
.rt tr.tot td{font-weight:700;background:var(--ground)}
.rsum{padding:12px 16px;display:grid;grid-template-columns:1fr auto;gap:6px 12px;font-size:15.5px;font-variant-numeric:tabular-nums}
.rsum .k{color:var(--ink-2)}.rsum .v{text-align:right;font-weight:600}
.rsum .net{font-size:18px;color:var(--ok);font-weight:700}
.rsum .fam{color:var(--urgent)}
.assume{padding:12px 16px 16px;font-size:14px;color:var(--ink-2);border-top:1px solid var(--line)}
.assume ul{margin:6px 0 0;padding-left:18px}
.verdict{border-radius:10px;padding:12px 14px;font-size:15.5px;display:none;gap:10px;align-items:flex-start}
.verdict.show{display:flex}
.verdict.good{background:var(--ok-soft);border:1px solid var(--ok)}
.verdict.plain{background:var(--brand-soft);border:1px solid var(--brand-2)}
.verdict.no{background:var(--bad-soft);border:1px solid var(--bad)}
.verdict .ic{flex:none;width:26px;height:26px;border-radius:50%;display:grid;place-items:center;font-weight:700;color:#fff}
.verdict.good .ic{background:var(--ok)}.verdict.plain .ic{background:var(--brand-2)}.verdict.no .ic{background:var(--bad)}


:root{
  --navy:#0F1F3D; --navy-2:#17305C; --gold:#C9A24A; --gold-soft:#F3E9CF;
  --brand:#1B3F8B; --brand-2:#2F8FD6; --brand-soft:#E7EFF6;
  --ground:#FAF9F5; --surface:#FFFFFF;
  --ink:#152238; --ink-2:#44536B; --ink-3:#6F7D93; --line:#E2DFD6;
  --urgent:#B8650E; --urgent-soft:#FDF2E3; --ok:#1E7A4E; --ok-soft:#E4F4EB; --bad:#B4322E; --bad-soft:#FBE9E7;
  --focus:#2F8FD6;
  --f-disp:"Noto Serif KR","IBM Plex Sans",serif;
  --f-body:"IBM Plex Sans","IBM Plex Sans KR","Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){color-scheme:dark;--navy:#0A1529;--navy-2:#122444;--gold:#D8B45E;--gold-soft:#3A3120;--brand:#7FB2F0;--brand-2:#5CB0EC;--brand-soft:#1B2A40;--ground:#0E1622;--surface:#162131;--ink:#E6ECF4;--ink-2:#AEBBCD;--ink-3:#8795AB;--line:#2A384C;--urgent:#F0A850;--urgent-soft:#2E2112;--ok:#5FCB93;--ok-soft:#14291E;--bad:#F28B85;--bad-soft:#36191A}}
:root[data-theme="dark"]{color-scheme:dark;--navy:#0A1529;--navy-2:#122444;--gold:#D8B45E;--gold-soft:#3A3120;--brand:#7FB2F0;--brand-2:#5CB0EC;--brand-soft:#1B2A40;--ground:#0E1622;--surface:#162131;--ink:#E6ECF4;--ink-2:#AEBBCD;--ink-3:#8795AB;--line:#2A384C;--urgent:#F0A850;--urgent-soft:#2E2112;--ok:#5FCB93;--ok-soft:#14291E;--bad:#F28B85;--bad-soft:#36191A}
*{box-sizing:border-box}
[hidden]{display:none!important}
html{scroll-behavior:smooth}
body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--f-body);font-size:16px;line-height:1.6;overflow-x:hidden}
h1,h2,h3{margin:0;line-height:1.3;text-wrap:balance;overflow-wrap:anywhere}
p{margin:0}
img{max-width:100%}
a{color:var(--brand)}
/* 단일 언어 표시 */
.t .mn,.t .ko{display:contents}
html.lang-mn .ko{display:none!important}
html.lang-ko .mn{display:none!important}
.wrap{max-width:1000px;margin:0 auto;padding-inline:20px}
.topbar{background:var(--surface);border-bottom:1px solid var(--line);position:sticky;top:env(safe-area-inset-top,0px);z-index:10}
.topbar .wrap{display:flex;align-items:center;gap:10px;padding-block:10px;flex-wrap:wrap}
.topbar img{height:38px;width:auto;display:block;flex:none}
.nav{display:flex;gap:2px;margin-left:auto;flex-wrap:wrap}
.nav a{font-size:15px;font-weight:600;color:var(--ink-2);text-decoration:none;padding:10px 10px;border-radius:8px;min-height:44px;display:inline-flex;align-items:center}
.nav a:hover,.nav a[aria-current="page"]{background:var(--ground);color:var(--ink)}
.lang{display:inline-flex;border:1px solid var(--line);border-radius:999px;background:var(--ground);padding:3px;gap:2px;flex:none}
.lang button{font:inherit;font-weight:700;font-size:14px;border:0;background:transparent;color:var(--ink-3);padding:8px 14px;border-radius:999px;cursor:pointer;min-height:40px}
.lang button[aria-pressed="true"]{background:var(--navy);color:#fff}
@media (max-width:480px){.topbar .wrap{gap:6px}.nav{width:100%;order:3;margin-left:0;justify-content:space-between}.nav a{padding:8px 6px;font-size:14px;flex:1;justify-content:center}}

.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;font:inherit;font-weight:700;font-size:16px;padding:12px 22px;min-height:48px;border-radius:10px;text-decoration:none;cursor:pointer;border:1px solid transparent;line-height:1.3;text-align:center;overflow-wrap:anywhere}
.btn.gold{background:var(--gold);color:#0F1F3D}
.btn.navy{background:var(--navy);color:#fff}
.btn.ghost{background:transparent;color:var(--ink);border-color:var(--line)}
.btn.ghost.onnavy{color:#fff;border-color:rgba(255,255,255,.4)}
.btn:disabled{opacity:.5;cursor:not-allowed}
.btn.block{width:100%}
.btn:focus-visible,button:focus-visible,a:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible,summary:focus-visible,[tabindex]:focus-visible{outline:3px solid var(--focus);outline-offset:2px}

section.sec{padding-block:44px}
.sec-h{margin-bottom:20px}
.sec-h h2{font-family:var(--f-disp);font-size:26px;font-weight:700}
.sec-h p{margin-top:8px;color:var(--ink-2);font-size:16px;max-width:64ch}
.lead{color:var(--ink-2);font-size:17px;max-width:60ch}
.eyebrow{font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:var(--gold);font-weight:700}
.note{font-size:14px;color:var(--ink-3)}
.callout{background:var(--urgent-soft);border-left:4px solid var(--urgent);border-radius:8px;padding:12px 14px;font-size:15px}
.callout.ok{background:var(--ok-soft);border-left-color:var(--ok)}
.callout.info{background:var(--brand-soft);border-left-color:var(--brand)}

.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
@media (max-width:760px){.grid3{grid-template-columns:1fr}}
@media (max-width:520px){.grid2{grid-template-columns:1fr}}
.item{min-width:0}
.item h3{font-size:18px;margin-bottom:6px}
.item p{color:var(--ink-2);font-size:15.5px}
.num{font-family:var(--f-disp);font-size:26px;font-weight:700;color:var(--gold);line-height:1;margin-bottom:8px}

.field{display:flex;flex-direction:column;gap:6px;min-width:0}
.field>label,.field>.lbl{font-weight:600;font-size:16px}
.req::after{content:" *";color:var(--bad)}
.field input,.field select,.field textarea{font:inherit;font-size:16px;color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:12px 14px;width:100%;min-width:0;min-height:48px}
.field textarea{min-height:88px;resize:vertical}
.hint{font-size:14px;color:var(--ink-3)}
.err{color:var(--bad);font-size:15px;font-weight:600;min-height:1.2em}
.seg{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.seg.three{grid-template-columns:repeat(3,1fr)}
.seg label{border:1px solid var(--line);border-radius:10px;padding:10px 12px;font-size:15.5px;cursor:pointer;display:flex;align-items:flex-start;gap:10px;background:var(--surface);min-width:0;line-height:1.35;min-height:48px}
.seg input{accent-color:var(--brand);margin:3px 0 0;flex:none;width:18px;height:18px;padding:0;border:0;min-height:0}
.seg label .t{flex:1;min-width:0;overflow-wrap:anywhere}
.seg label:has(input:checked){border-color:var(--brand);background:var(--brand-soft);color:var(--brand);font-weight:600}
@media (max-width:420px){.seg.three{grid-template-columns:1fr 1fr}}
.won{position:relative}
.won input{padding-right:40px!important;text-align:right;font-variant-numeric:tabular-nums}
.won span{position:absolute;right:14px;top:50%;transform:translateY(-50%);color:var(--ink-3);font-size:14px;pointer-events:none}

footer{background:var(--surface);border-top:1px solid var(--line);padding-block:28px 44px;font-size:14px;color:var(--ink-3)}
footer .wrap{display:flex;flex-direction:column;gap:6px}
footer b{color:var(--ink-2);font-weight:600}

.hero{background:var(--navy);color:#fff}
.hero .wrap{display:grid;grid-template-columns:1.4fr .6fr;gap:32px;align-items:center;padding-block:52px 44px}
.hero h1{font-family:var(--f-disp);font-size:36px;font-weight:700;color:#fff;margin-top:12px}
.hero .lead{color:rgba(255,255,255,.82);margin-top:16px}
.hero .cta{display:flex;flex-wrap:wrap;gap:10px;margin-top:24px}
.fees{display:flex;flex-wrap:wrap;gap:8px 18px;margin-top:18px;font-size:15px;color:rgba(255,255,255,.85)}
.fees b{color:var(--gold)}
.profile{display:flex;flex-direction:column;align-items:center;text-align:center;gap:12px;background:rgba(255,255,255,.06);border:1px solid rgba(201,162,74,.45);border-radius:16px;padding:18px;max-width:300px;justify-self:end}
.profile img{width:100%;max-width:240px;aspect-ratio:1;border-radius:14px;object-fit:cover;object-position:50% 15%;border:2px solid var(--gold)}
.profile b{display:block;font-family:var(--f-disp);font-size:20px;color:#fff}
.profile span{display:block;font-size:14px;color:rgba(255,255,255,.72);margin-top:2px}
@media (max-width:760px){.hero .wrap{grid-template-columns:1fr;gap:22px;padding-block:36px 30px}.hero h1{font-size:28px}
  .profile{flex-direction:row;text-align:left;max-width:none;justify-self:stretch;padding:12px 14px}.profile img{width:72px;max-width:72px;height:72px;border-radius:50%}.profile b{font-size:17px}}
.alt{background:var(--surface);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.who{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:12px}
.who li{display:flex;gap:12px;align-items:flex-start;font-size:16px}
.who li::before{content:"✓";flex:none;width:26px;height:26px;border-radius:50%;background:var(--ok-soft);color:var(--ok);font-weight:700;display:grid;place-items:center;margin-top:2px}
@media (max-width:640px){.who{grid-template-columns:1fr}}
.calc-band{background:var(--navy);color:#fff;border-radius:16px;padding:28px 24px;display:flex;gap:20px;align-items:center;justify-content:space-between;flex-wrap:wrap}
.calc-band h2{font-family:var(--f-disp);font-size:24px;color:#fff}
.calc-band p{color:rgba(255,255,255,.8);margin-top:8px;max-width:56ch}
.people{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.person{display:flex;gap:14px;align-items:flex-start;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:16px}
.person img,.person .ava{width:64px;height:64px;border-radius:50%;flex:none;object-fit:cover;object-position:50% 20%}
.person .ava{background:var(--gold-soft);color:var(--navy);display:grid;place-items:center;font-family:var(--f-disp);font-weight:700;font-size:20px}
.person b{display:block;font-size:17px}
.person span{display:block;font-size:14px;color:var(--ink-3)}
.person p{margin-top:6px;font-size:15px;color:var(--ink-2)}
@media (max-width:640px){.people{grid-template-columns:1fr}}
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;counter-reset:s}
.step{counter-increment:s;min-width:0}
.step::before{content:"0" counter(s);font-family:var(--f-disp);font-size:24px;font-weight:700;color:var(--gold);line-height:1;display:block;margin-bottom:8px}
.step h3{font-size:17px}
.step p{margin-top:6px;font-size:15px;color:var(--ink-2)}
@media (max-width:760px){.steps{grid-template-columns:1fr 1fr}}
@media (max-width:420px){.steps{grid-template-columns:1fr}}
.faq details{border-top:1px solid var(--line);padding:14px 0}
.faq details:last-of-type{border-bottom:1px solid var(--line)}
.faq summary{font-weight:600;cursor:pointer;list-style:none;display:flex;justify-content:space-between;gap:12px;font-size:16.5px;min-height:32px;align-items:center}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";color:var(--gold);font-size:22px;line-height:1;flex:none}
.faq details[open] summary::after{content:"−"}
.faq .a{margin-top:10px;color:var(--ink-2);font-size:15.5px;max-width:70ch}
.acct{font-variant-numeric:tabular-nums;font-weight:700;color:var(--ink)}
.contact{background:var(--navy);color:#fff;border-radius:16px;padding:26px 22px}
.contact h2{font-family:var(--f-disp);font-size:24px;color:#fff}
.contact p{color:rgba(255,255,255,.8);margin-top:8px;max-width:56ch}
.contact .cta{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px}
.contact .tel{margin-top:16px;font-size:15px;color:rgba(255,255,255,.75)}
.contact .tel b{color:#fff;font-size:18px;font-variant-numeric:tabular-nums}
.contact button.copy{font:inherit;font-size:13px;border:1px solid rgba(255,255,255,.35);background:transparent;color:#fff;border-radius:6px;padding:5px 10px;cursor:pointer;margin-left:8px;min-height:32px}

/* v3 design layer — append after the existing styles */
:root,:root[data-theme]{color-scheme:light;--navy:#1b2a4a;--navy-2:#263958;--gold:#d5b366;--ground:#f7f5ef;--surface:#fff;--ink:#202c40;--ink-2:#505e70;--ink-3:#626e7c;--line:#dce0e4;--brand:#1b2a4a;--brand-2:#526785;--brand-soft:#edf1f6;--ok:#246347;--ok-soft:#edf5ef;--bad:#ab3030;--bad-soft:#faeded;--urgent:#85521d;--urgent-soft:#f6f0e7;--f-body:system-ui,-apple-system,"Segoe UI","Malgun Gothic",Arial,sans-serif;--f-disp:var(--f-body)}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]){color-scheme:light;--navy:#1b2a4a;--navy-2:#263958;--gold:#d5b366;--ground:#f7f5ef;--surface:#fff;--ink:#202c40;--ink-2:#505e70;--ink-3:#626e7c;--line:#dce0e4;--brand:#1b2a4a;--brand-2:#526785;--brand-soft:#edf1f6;--ok:#246347;--ok-soft:#edf5ef;--bad:#ab3030;--bad-soft:#faeded;--urgent:#85521d;--urgent-soft:#f6f0e7}}
*,*::before,*::after{box-sizing:border-box}
body{font-size:16px;line-height:1.6;overflow-x:visible;overflow-wrap:anywhere}
[hidden]{display:none!important}
.t .mn,.t .ko{display:contents}
html.lang-mn .ko{display:none!important}
html.lang-ko .mn{display:none!important}
button,input,select,textarea{font-family:var(--f-body)}
button,.btn{min-height:48px;white-space:normal;overflow-wrap:anywhere}
.wrap{max-width:1120px;padding-inline:24px}
.topbar{position:relative;top:auto}
.topbar .wrap{gap:12px;padding-block:12px}
.topbar img{max-width:160px;height:auto;max-height:42px;object-fit:contain}
.nav{min-width:0;gap:4px}
.nav a{min-width:0;line-height:1.35;text-align:center;white-space:normal}
.lang{margin-left:auto;border:0;border-radius:8px}
.lang button{min-height:48px;border-radius:6px;padding:8px 12px}
.btn{border-radius:8px;padding:14px 20px;line-height:1.45;max-width:100%}
.btn.ghost{border-color:#aeb7c2}
.btn.ghost.onnavy{border-color:#8390a5}
.hero .wrap{grid-template-columns:minmax(0,1.35fr) minmax(0,.8fr);gap:48px;padding-block:56px}
.hero h1{font-size:40px;line-height:1.25;letter-spacing:-.025em}
.hero .lead{font-size:17px;line-height:1.65;color:#e2e7ef}
.hero .eyebrow{color:#c7d0de;letter-spacing:.06em}
.hero .cta{gap:12px;margin-top:24px}
.fees{font-size:16px;color:#d8e0ed;gap:8px 20px}
.profile{width:100%;max-width:340px;padding:0;border:0;background:none;border-radius:0;gap:16px}
.profile img{width:100%;max-width:340px;border:0;border-radius:10px;aspect-ratio:320/309}
.profile span{font-size:16px;color:#c7d0de}
section.sec{padding-block:56px}
.sec-h{margin-bottom:28px}
.sec-h h2{font-size:30px;letter-spacing:-.025em}
.eyebrow,.num,.step::before,.faq summary::after{color:var(--navy)}
.who{gap:20px 32px;grid-template-columns:repeat(2,minmax(0,1fr))}
.people{grid-template-columns:repeat(2,minmax(0,1fr));gap:28px}
.person{min-width:0;padding:22px 0;border:0;border-top:1px solid var(--line);border-radius:0;background:none;gap:18px}
.person>div{min-width:0;flex:1}
.person img,.person .ava{width:72px;height:72px}
.person .ava{background:var(--brand-soft);color:var(--navy)}
.person b{font-size:19px}
.person span,.person p{font-size:16px}
.steps{gap:24px}
.step{padding-top:20px;border-top:1px solid var(--line)}
.step h3{font-size:18px}
.step p,.faq .a,.item p{font-size:16px}
.calc-band,.contact{border-radius:10px;padding:30px}
.calc-band>div{min-width:0;flex:1 1 320px}
.calc-band .btn{flex:0 1 auto}
.contact .tel,.contact button.copy{font-size:16px}
.contact button.copy{min-height:48px;margin-top:8px;padding:10px 14px}
.callout{border-radius:6px;padding:16px;border-left-width:3px;font-size:16px}
.note,.hint,.slot-sub,.dz,.assume,.prog,.err,footer{font-size:16px}
.page{max-width:820px;padding:36px 24px 72px}
.page-h h1{font-size:32px;letter-spacing:-.025em}
.page-h p{margin-top:12px;max-width:65ch}
.form{gap:24px}
.grid2{grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}
.grid2>*{min-width:0}
.field{gap:8px}
.field input,.field select,.field textarea{min-height:52px;border-color:#aeb7c2;border-radius:7px;font-size:16px;padding:12px}
.field textarea{min-height:104px}
.seg{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.seg label{font-size:16px;border-radius:7px;padding:14px 12px;line-height:1.5}
.seg input,.field .seg input{width:20px;height:20px;min-height:0;padding:0;flex:none}
.seg input:checked+.t{font-weight:700;color:var(--brand)}
.paytools .won{min-width:0}
.chk{font-size:16px;min-height:48px}
.years{gap:10px;grid-template-columns:repeat(5,minmax(0,1fr))}
.years .y input{font-size:16px;min-height:52px}
.years .y small{font-size:16px}
.extra{padding:18px 0;border:0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);border-radius:0}
.extra summary,.faq summary{min-height:48px}
.result{display:flex;flex-direction:column;min-width:0;border:0;border-radius:10px}
.rhead{order:0;padding:24px;color:#fff}
.rhead .lbl2{font-size:16px;opacity:1;color:#e2e7ef}
.rhead .big{margin-top:10px;color:var(--gold);font-size:40px;letter-spacing:-.03em}
.rsum{order:1;padding:24px;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px;font-size:16px}
.rsum>*{min-width:0}
.rsum .net{border-top:1px solid var(--line);padding-top:16px;color:var(--navy);font-size:18px}
.rsum .v.net{font-size:28px;line-height:1.3}
.tblwrap{order:2;min-width:0;max-width:100%;padding:0 16px;overflow:visible}
.rt{table-layout:fixed;font-size:14px}
.rt th,.rt td{white-space:normal;overflow-wrap:anywhere;padding:12px 5px;vertical-align:top}
.rt th{font-size:14px}
.rt th:first-child{width:14%}
.assume{order:3;margin-top:16px;padding:20px 24px}
.verdict{font-size:16px;border-radius:8px}
.verdict>div{min-width:0}
.stepbar{gap:12px;margin:28px 0 24px;grid-template-columns:repeat(3,minmax(0,1fr))}
.stepbar>div{padding:14px 6px 12px;border-top:4px solid #c5ccd5;font-size:16px;word-break:normal;overflow-wrap:anywhere;background:transparent;border-radius:0}
.stepbar>div.cur{border-top-color:var(--navy);background:var(--brand-soft);color:var(--navy)}
.stepbar>div.done{border:0;border-top:4px solid var(--ok);padding:14px 6px 12px;color:var(--ok);background:transparent;border-radius:0}
.navrow{gap:12px;margin-top:16px}
.navrow .btn{min-width:0;flex:1 1 140px}
.form h2{font-size:24px}
.form h3{font-size:19px}
.req::after,.req-tag{font-size:20px;font-weight:700;color:var(--bad)}
.slots{gap:22px}
.slot{border:0;border-bottom:1px solid var(--line);border-radius:0;padding:20px 0;background:transparent;min-width:0}
.slot.ok{border-bottom:2px solid var(--ok)}
.slot.over{outline:3px dashed var(--brand);outline-offset:6px;border-bottom-style:solid;background:var(--brand-soft)}
.slot-h{margin-bottom:8px}
.slot-b{gap:10px}
label.file{flex:1 1 150px;justify-content:center;text-align:center;min-width:0;min-height:52px;border-radius:8px;font-size:16px;padding:14px 12px;line-height:1.5}
label.file.cam{flex-basis:100%;min-height:84px;border:2px dashed #8799b0;background:var(--brand-soft)}
label.file:focus-within{outline:3px solid var(--focus);outline-offset:3px}
.dz{padding-top:8px}
.flist li{flex-wrap:wrap;font-size:16px;padding:10px}
.flist li .nm{flex:1 1 90px;white-space:normal;overflow-wrap:anywhere}
.flist li button{min-width:48px;min-height:48px}
.summary{grid-template-columns:minmax(0,1fr) minmax(0,2fr);font-size:16px;border:0;border-radius:8px;padding:20px;gap:14px 20px}
.agree{font-size:16px;border:0;border-top:1px solid var(--line);border-radius:0;padding:20px 0;background:transparent}
.agree>div{min-width:0;flex:1}
.agree details{font-size:16px}
.agree summary{min-height:48px;padding-block:10px}
.proxy{font-size:16px;border:0;border-radius:8px;padding:18px;background:var(--brand-soft)}
.proxy .field input{width:100%;height:auto;min-height:52px}
.pw{background:var(--brand-soft);border-radius:8px;padding:18px;gap:16px}
.pwrow{display:flex;gap:8px;align-items:stretch;min-width:0}
.pwrow input{flex:1;min-width:0;padding-right:12px!important}
.pwrow button{position:static;transform:none;flex:none;font-size:16px;min-height:52px;padding:10px 12px}
section.done{border:0;padding:30px 24px;border-radius:10px}
footer{padding-block:32px 44px}
footer .wrap{gap:10px}
@media(max-width:900px){.topbar .wrap{flex-wrap:wrap;justify-content:space-between}.topbar .wrap>a{max-width:45%}.nav{order:3;width:100%;margin:0;justify-content:space-between;border-top:1px solid var(--line);padding-top:6px}.nav a{flex:1;padding:8px 6px;min-height:48px;font-size:14px}.hero .wrap{grid-template-columns:minmax(0,1fr);gap:24px;padding-block:28px}.hero h1{font-size:30px}.profile{flex-direction:row;align-items:center;text-align:left;justify-self:stretch;max-width:none}.profile img{width:72px;max-width:72px;height:72px;flex:none;border-radius:8px}.profile b{font-size:18px}.hero .cta{flex-direction:column}.hero .cta .btn{width:100%}.hero .lead{font-size:16px}.hero h1 br{display:none}}
@media(max-width:640px){.wrap{padding-inline:18px}.page{padding:28px 18px 56px}.topbar .wrap{gap:6px}.topbar img{max-width:132px;max-height:36px}.lang button{padding:8px 10px}.hero h1{font-size:27px}.hero .wrap{padding-block:24px}.hero .lead{margin-top:14px}.hero .cta{margin-top:18px;gap:10px}.fees{margin-top:16px}.people,.who,.grid2{grid-template-columns:minmax(0,1fr)}.people{gap:8px}.person{gap:14px}.person img,.person .ava{width:64px;height:64px}.sec-h h2{font-size:26px}section.sec{padding-block:36px}.calc-band,.contact{padding:24px 18px}.calc-band .btn{width:100%}.page-h h1{font-size:28px}.seg.three{grid-template-columns:minmax(0,1fr)}.years{grid-template-columns:repeat(2,minmax(0,1fr))}.rhead,.rsum{padding:20px 16px}.rhead .big{font-size:32px}.rsum .k.net,.rsum .v.net{grid-column:1/-1}.rsum .v.net{border-top:0;padding-top:0;text-align:left;font-size:30px}.tblwrap{padding-inline:8px}.rt,.rt th{font-size:12px}.rt th,.rt td{padding:10px 3px}.assume{padding:18px 16px}.stepbar{gap:8px}.stepbar>div,.stepbar>div.done{padding:12px 4px}.summary{grid-template-columns:minmax(0,1fr);gap:6px;padding:18px}.summary dd{margin-bottom:12px}.pw{padding:16px 12px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*,*::before,*::after{transition:none!important;animation:none!important}}

/* 수정: 월급 행 — 단위 겹침·체크박스 크기 */
.paytools{align-items:center}
.paytools .won{flex:1 1 200px;min-width:0}
.paytools .won input{padding-right:72px!important}
.paytools .won span{white-space:nowrap;right:12px}
.won > span span{position:static;transform:none;display:inline;right:auto;top:auto}
.chk{flex:0 0 auto;white-space:nowrap}
.chk input,.field .chk input{width:20px;height:20px;min-height:0;min-width:0;padding:0;margin:0;flex:none}
"""

def shell(title, body, extra_css='', js='', current=''):
    def nav(href, mn, ko, key):
        cur = ' aria-current="page"' if key == current else ''
        return f'<a href="{href}"{cur}>{T(mn,ko)}</a>'
    return f'''<!doctype html>
<html lang="mn" class="lang-mn">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<style>{CSS}{extra_css}</style>
<script src="config.js"></script>
</head>
<body>
<header class="topbar">
  <div class="wrap">
    <a href="index.html" style="display:block;flex:none"><img src="{LOGO}" alt="세무법인 위드택스"></a>
    <nav class="nav" aria-label="메뉴">
      {nav('index.html','Нүүр','홈','index')}
      {nav('calc.html','Буцаалтын тооцоо','예상 환급액 계산','calc')}
      {nav('apply.html','Онлайн бүртгэл','온라인 접수','apply')}
    </nav>
    <div class="lang" role="group" aria-label="Хэл / 언어">
      <button type="button" id="btnMn" aria-pressed="true" lang="mn">Монгол</button>
      <button type="button" id="btnKo" aria-pressed="false" lang="ko">한국어</button>
    </div>
  </div>
</header>
{body}
<footer>
  <div class="wrap">
    <div><b>세무법인 위드택스</b> · {T('Сөүл, Каннам-гү, Ёксам-дон','서울특별시 강남구 역삼동')} · {T('Тэргүүн татварын мэргэжилтэн Юн Дун Ин','대표세무사 윤동인')} · 02-536-1260</div>
    <div>{T('Хариуцсан татварын мэргэжилтэн Пак Гён Жүн · Монгол хэлний хариуцагч Хан Са Ра','담당 세무사 박경준 · 몽골어 담당 한사라')}</div>
    <div>{T('Энэ сайтын тооцоо нь урьдчилсан дүн бөгөөд бодит буцаалт нь цалингийн татварын тодорхойлолт зэрэг баримтаар дахин тооцогдоно.','본 사이트의 계산 결과는 추정치이며, 실제 환급액은 원천징수영수증 등 자료를 기준으로 재계산됩니다.')}</div>
  </div>
</footer>
<script>
(function(){{
  const root=document.documentElement;
  const Y=[2021,2022,2023,2024,2025];
  const L=()=>root.classList.contains('lang-ko')?'ko':'mn';
  function setLang(l){{
    root.classList.toggle('lang-ko',l==='ko');root.classList.toggle('lang-mn',l!=='ko');root.lang=l==='ko'?'ko':'mn';
    document.getElementById('btnMn').setAttribute('aria-pressed',l!=='ko');
    document.getElementById('btnKo').setAttribute('aria-pressed',l==='ko');
    document.querySelectorAll('[data-ph-mn]').forEach(el=>{{el.placeholder=l==='ko'?el.dataset.phKo:el.dataset.phMn;}});
    document.querySelectorAll('option[data-mn]').forEach(o=>{{o.textContent=l==='ko'?o.dataset.ko:o.dataset.mn;}});
    try{{localStorage.setItem('lang',l)}}catch(e){{}}
    if(typeof onLang==='function')onLang(l);
  }}
  document.getElementById('btnMn').onclick=()=>setLang('mn');
  document.getElementById('btnKo').onclick=()=>setLang('ko');
{js}
  let l0='mn'; try{{l0=localStorage.getItem('lang')||'mn'}}catch(e){{}} setLang(l0);
}})();
</script>
</body>
</html>
'''

# ============================== INDEX ==============================
INDEX_CSS = r"""
.hero{background:var(--navy);color:#fff}
.hero .wrap{display:grid;grid-template-columns:1.4fr .6fr;gap:32px;align-items:center;padding-block:52px 44px}
.hero h1{font-family:var(--f-disp);font-size:36px;font-weight:700;color:#fff;margin-top:12px}
.hero .lead{color:rgba(255,255,255,.82);margin-top:16px}
.hero .cta{display:flex;flex-wrap:wrap;gap:10px;margin-top:24px}
.fees{display:flex;flex-wrap:wrap;gap:8px 18px;margin-top:18px;font-size:15px;color:rgba(255,255,255,.85)}
.fees b{color:var(--gold)}
.profile{display:flex;flex-direction:column;align-items:center;text-align:center;gap:12px;background:rgba(255,255,255,.06);border:1px solid rgba(201,162,74,.45);border-radius:16px;padding:18px;max-width:300px;justify-self:end}
.profile img{width:100%;max-width:240px;aspect-ratio:1;border-radius:14px;object-fit:cover;object-position:50% 15%;border:2px solid var(--gold)}
.profile b{display:block;font-family:var(--f-disp);font-size:20px;color:#fff}
.profile span{display:block;font-size:14px;color:rgba(255,255,255,.72);margin-top:2px}
@media (max-width:760px){.hero .wrap{grid-template-columns:1fr;gap:22px;padding-block:36px 30px}.hero h1{font-size:28px}
  .profile{flex-direction:row;text-align:left;max-width:none;justify-self:stretch;padding:12px 14px}.profile img{width:72px;max-width:72px;height:72px;border-radius:50%}.profile b{font-size:17px}}
.alt{background:var(--surface);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.who{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:12px}
.who li{display:flex;gap:12px;align-items:flex-start;font-size:16px}
.who li::before{content:"✓";flex:none;width:26px;height:26px;border-radius:50%;background:var(--ok-soft);color:var(--ok);font-weight:700;display:grid;place-items:center;margin-top:2px}
@media (max-width:640px){.who{grid-template-columns:1fr}}
.calc-band{background:var(--navy);color:#fff;border-radius:16px;padding:28px 24px;display:flex;gap:20px;align-items:center;justify-content:space-between;flex-wrap:wrap}
.calc-band h2{font-family:var(--f-disp);font-size:24px;color:#fff}
.calc-band p{color:rgba(255,255,255,.8);margin-top:8px;max-width:56ch}
.people{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.person{display:flex;gap:14px;align-items:flex-start;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:16px}
.person img,.person .ava{width:64px;height:64px;border-radius:50%;flex:none;object-fit:cover;object-position:50% 20%}
.person .ava{background:var(--gold-soft);color:var(--navy);display:grid;place-items:center;font-family:var(--f-disp);font-weight:700;font-size:20px}
.person b{display:block;font-size:17px}
.person span{display:block;font-size:14px;color:var(--ink-3)}
.person p{margin-top:6px;font-size:15px;color:var(--ink-2)}
@media (max-width:640px){.people{grid-template-columns:1fr}}
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;counter-reset:s}
.step{counter-increment:s;min-width:0}
.step::before{content:"0" counter(s);font-family:var(--f-disp);font-size:24px;font-weight:700;color:var(--gold);line-height:1;display:block;margin-bottom:8px}
.step h3{font-size:17px}
.step p{margin-top:6px;font-size:15px;color:var(--ink-2)}
@media (max-width:760px){.steps{grid-template-columns:1fr 1fr}}
@media (max-width:420px){.steps{grid-template-columns:1fr}}
.faq details{border-top:1px solid var(--line);padding:14px 0}
.faq details:last-of-type{border-bottom:1px solid var(--line)}
.faq summary{font-weight:600;cursor:pointer;list-style:none;display:flex;justify-content:space-between;gap:12px;font-size:16.5px;min-height:32px;align-items:center}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";color:var(--gold);font-size:22px;line-height:1;flex:none}
.faq details[open] summary::after{content:"−"}
.faq .a{margin-top:10px;color:var(--ink-2);font-size:15.5px;max-width:70ch}
.acct{font-variant-numeric:tabular-nums;font-weight:700;color:var(--ink)}
.contact{background:var(--navy);color:#fff;border-radius:16px;padding:26px 22px}
.contact h2{font-family:var(--f-disp);font-size:24px;color:#fff}
.contact p{color:rgba(255,255,255,.8);margin-top:8px;max-width:56ch}
.contact .cta{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px}
.contact .tel{margin-top:16px;font-size:15px;color:rgba(255,255,255,.75)}
.contact .tel b{color:#fff;font-size:18px;font-variant-numeric:tabular-nums}
.contact button.copy{font:inherit;font-size:13px;border:1px solid rgba(255,255,255,.35);background:transparent;color:#fff;border-radius:6px;padding:5px 10px;cursor:pointer;margin-left:8px;min-height:32px}
"""

def INDEX():
    body = f'''
<section class="hero">
  <div class="wrap">
    <div>
      <div class="eyebrow">세무법인 위드택스</div>
      <h1>{T('Солонгост төлсөн цалингийн татвараа буцаан авах боломжтой эсэхээ шалгаарай.','한국에서 낸 근로소득세,<br>돌려받을 수 있는지 확인하세요.')}</h1>
      <p class="lead">{T('Татварын мэргэжилтэн буцаалт авах боломжтой эсэх, урьдчилсан дүнг шалгаж, та зөвшөөрвөл мэдүүлгийг таны өмнөөс гаргана. Монгол хэлний хариуцагч баримт бэлтгэхээс эхлээд үр дүн хүртэл тусална.','세무사가 환급 가능 여부와 예상 금액을 검토하고, 신청에 동의하시면 신고를 대행합니다. 몽골어 담당자가 자료 준비부터 결과 안내까지 도와드립니다.')}</p>
      <div class="cta">
        <a class="btn gold" href="calc.html">{T('Урьдчилсан буцаалтаа тооцоолох','예상 환급액 계산하기')}</a>
        <a class="btn ghost onnavy" href="#contact">{T('Монголоор зөвлөгөө авах','몽골어로 상담하기')}</a>
      </div>
      <div class="fees">
        <span>{T('Буцаалт гарвал хураамж <b>22%</b> · НӨАТ орсон','환급 시 수수료 <b>22%</b> · 부가세 포함')}</span>
        <span>{T('Буцаалт байхгүй бол хураамж <b>0 ₩</b>','환급이 없으면 수수료 <b>0원</b>')}</span>
      </div>
    </div>
    <div class="profile">
      <img src="{PHOTO}" alt="박경준 세무사">
      <div><b>박경준 {T('Татварын мэргэжилтэн','세무사')}</b><span>{T('Хариуцсан мэргэжилтэн · 세무법인 위드택스','담당 세무사 · 세무법인 위드택스')}</span></div>
    </div>
  </div>
</section>

<section class="sec alt">
  <div class="wrap">
    <div class="sec-h"><h2>{T('Хэн буцаалтын шалгалт хийлгэж болох вэ','어떤 분이 환급 검토를 받을 수 있나요')}</h2>
      <p>{T('Доорх нөхцөлд хамаарвал шалгуулж үзэх нь зүйтэй. Гадаад иргэн гэдэг нь дангаараа буцаалтын үндэслэл болохгүй.','아래에 해당하면 검토해 볼 만합니다. 외국인이라는 이유만으로 환급 대상이 되는 것은 아닙니다.')}</p></div>
    <ul class="who">
      <li>{T('2021 оноос хойш Солонгост цалинтай ажилласан','2021년 이후 한국에서 급여를 받고 근무한 경험이 있음')}</li>
      <li>{T('Цалингаас орлогын албан татвар суутгагдаж байсан (цалингийн хуудас, тодорхойлолтоос харагдана)','급여에서 근로소득세가 원천징수된 적이 있음 (급여명세·원천징수영수증에서 확인)')}</li>
      <li>{T('Жилийн эцсийн тооцоонд эмнэлгийн зардал, даатгал зэрэг хасалт тусгагдаагүй байж болзошгүй','연말정산에서 의료비·보험료 등 공제가 빠졌을 가능성이 있음')}</li>
      <li>{T('Жижиг дунд үйлдвэрт залуу насандаа ажилд орсон ч татварын хөнгөлөлт хэрэглэгдээгүй байж болзошгүй','중소기업에 젊은 나이에 취업했지만 소득세 감면이 적용되지 않았을 가능성이 있음')}</li>
    </ul>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="calc-band">
      <div>
        <h2>{T('Энгийн мэдээлэл оруулаад урьдчилсан буцаалтаа хараарай','간단한 입력으로 예상 환급액 확인')}</h2>
        <p>{T('Ажилд орсон хугацаа, тэр үеийн нас, компанийн салбар, цалингаа оруулна уу. Урьдчилсан тооцоо үнэгүй. Тооцоолсны дараа бүртгүүлэх эсэхээ шийднэ үү.','취업 시기·당시 나이·회사 업종·급여를 입력하세요. 예상액 계산은 무료입니다. 계산 후 신청 여부를 결정하세요.')}</p>
      </div>
      <a class="btn gold" href="calc.html">{T('Тооцоолох','예상 환급액 계산하기')}</a>
    </div>
  </div>
</section>

<section class="sec alt">
  <div class="wrap">
    <div class="sec-h"><h2>{T('Хариуцсан мэргэжилтэн ба хариуцагч','담당 세무사와 몽골어 담당자')}</h2></div>
    <div class="people">
      <div class="person"><img src="{PHOTO}" alt="박경준 세무사"><div><b>박경준 {T('Татварын мэргэжилтэн','세무사')}</b><span>세무법인 위드택스</span>
        <p>{T('Буцаалт авах боломжтой эсэхийг шалгаж, Хоумтакс дээр татварын төлөөлөгчөөр бүртгүүлэн таны нэрээр мэдүүлэг гаргана. Бүртгэлийн баримтыг (접수증) танд өгнө.','환급 가능 여부를 검토하고 홈택스 세무대리 수임 후 본인 명의로 신고합니다. 국세청 접수증을 전달합니다.')}</p></div></div>
      <div class="person"><div class="ava">MN</div><div><b>한사라</b><span>{T('Монгол хэлний хариуцагч','몽골어 담당자')}</span>
        <p>{T('Баримт цуглуулах, асуулт хариулт, үр дүн мэдэгдэх хүртэл монгол хэлээр тусална.','자료 준비부터 질문 응대, 결과 안내까지 몽골어로 도와드립니다.')}</p></div></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-h"><h2>{T('Буцаалт боломжтой эсэхээс мэдүүлэг хүртэл — ингэж тусална','환급 가능 여부부터 신고까지, 이렇게 도와드립니다')}</h2></div>
    <div class="steps">
      <div class="step"><h3>{T('Баримт илгээх','자료 제출')}</h3><p>{T('Шаардлагатай баримт, илгээх аргыг заавар болгоно.','필요한 자료와 제출 방법을 안내합니다.')}</p></div>
      <div class="step"><h3>{T('Шалгалтын үр дүн','검토 결과 안내')}</h3><p>{T('Шаардлагатай баримт бүгд баталгаажсанаас хойш 3 ажлын өдрийн дотор урьдчилсан буцаалт, хураамжийг мэдэгдэнэ.','필요한 자료가 모두 확인되면 영업일 3일 이내 예상 환급액과 수수료를 안내합니다.')}</p></div>
      <div class="step"><h3>{T('Зөвшөөрлийн дараа мэдүүлэг','동의 후 신고')}</h3><p>{T('Үр дүнг шалгаад зөвшөөрвөл мэдүүлгийг гаргана.','검토 결과를 확인하고 신청에 동의하시면 신고를 진행합니다.')}</p></div>
      <div class="step"><h3>{T('Буцаалт ба хураамж','환급 및 수수료 지급')}</h3><p>{T('Буцаалт дансанд орсныг баталгаажуулсны дараа мэдэгдсэн хураамжийг төлнө.','환급금 입금 확인 후 안내된 수수료를 지급합니다.')}</p></div>
    </div>
    <div class="callout info" style="margin-top:18px">{T('Хураамж: буцаалтын дүнгийн 22% (НӨАТ орсон). Буцаалт байхгүй бол хураамж 0. Хураамжийг зөвхөн буцаалт орсны дараа төлнө.','수수료: 환급액의 22%(부가세 포함). 환급이 없으면 수수료 0원. 수수료는 환급금 입금 확인 후에만 지급합니다.')}</div>
  </div>
</section>

<section class="sec alt faq">
  <div class="wrap">
    <div class="sec-h"><h2>{T('Түгээмэл асуулт','자주 묻는 질문')}</h2></div>
    <details><summary>{T('Буцаалт хэзээ орох вэ?','환급은 언제 들어오나요?')}</summary><div class="a">{T('Мэдүүлгээс хойш буцаалт хүртэл ойролцоогоор 2 сар гэж тооцдог бөгөөд татварын албаны шалгалтаас хамаарч өөрчлөгдөж болно. Татварын алба таны дансанд шууд шилжүүлнэ.','신고 후 환급까지 약 2개월이 예상되며, 심사 상황에 따라 달라질 수 있습니다. 국세청이 본인 계좌로 직접 입금합니다.')}</div></details>
    <details><summary>{T('Хураамжийг хэзээ, хаана төлөх вэ?','수수료는 언제 어디로 내나요?')}</summary><div class="a">{T('Буцаалт дансанд орсныг баталгаажуулсны дараа. Данс: 신한은행 <span class="acct">140-016-484564</span> (эзэмшигч: 세무법인 위드택스). Өөр данс заасан тохиолдолд шууд утсаар баталгаажуулна уу.','환급 입금 확인 후 신한은행 <span class="acct">140-016-484564</span>(예금주: 세무법인 위드택스)로 지급합니다. 다른 계좌를 안내받으면 바로 확인 전화 주세요.')}</div></details>
    <details><summary>{T('Хэдэн оны татварыг буцаан авч болох вэ?','몇 년도분까지 신청할 수 있나요?')}</summary><div class="a">{T('Буцаалт хүсэх хугацаа нь оноос хамаарч ялгаатай (мэдүүлгийн төрөл, хувь хүний нөхцөлөөс хамаарна). Ерөнхийдөө 2021 оноос хойшхи жилүүдийг шалгадаг бөгөөд 2020 ба өмнөх он ихэнх тохиолдолд хамаарахгүй. Тодорхой хугацааг баримт шалгасны дараа мэдэгдэнэ.','신청 가능 기한은 귀속연도와 신고 유형, 개인 사정에 따라 다릅니다. 일반적으로 2021년 이후분을 검토하며, 2020년 이전분은 대부분 기한이 지났습니다. 정확한 기한은 자료 확인 후 안내합니다.')}</div></details>
    <details><summary>{T('Компани мэдэх үү?','회사에 알려지나요?')}</summary><div class="a">{T('Таны нэрээр мэдүүлнэ. Компанийн баримт шалгах шаардлага гарвал урьдчилан мэдэгдэнэ.','본인 명의로 신청합니다. 회사 자료 확인이 필요한 경우에는 사전에 안내합니다.')}</div></details>
    <details><summary>{T('Виз, оршин суухтай холбоотой юу?','비자나 체류와 관련이 있나요?')}</summary><div class="a">{T('Энэ бол цалингийн орлогын албан татварын буцаалт хүсэх журам юм. Оршин суухтай холбоотой асуултыг тусад нь лавлана уу.','근로소득세 환급을 신청하는 절차입니다. 체류 관련 문의는 별도로 확인해 주세요.')}</div></details>
    <details><summary>{T('Хоумтакс нэвтрэх мэдээлэл яагаад хэрэгтэй вэ?','홈택스 로그인 정보는 왜 필요한가요?')}</summary><div class="a">{T('Жилийн эцсийн тооцооны баримтыг (간소화자료) зөвхөн таны бүртгэлээр авах боломжтой. Бүртгэлийн дараа хариуцагч ашиглах арга, зөвшөөрлийн талаар тусад нь тайлбарлана.','연말정산 간소화자료는 본인 계정으로만 조회할 수 있습니다. 접수 후 담당자가 조회 방법과 수임동의 절차를 별도로 안내합니다.')}</div></details>
  </div>
</section>

<section class="sec" id="contact">
  <div class="wrap">
    <div class="contact">
      <h2>{T('Зөвлөгөө авах, бүртгүүлэх','상담과 접수')}</h2>
      <p>{T('Эхлээд монгол хэлээр асуугаарай. Бэлэн бол онлайнаар шууд бүртгүүлж болно.','먼저 몽골어로 물어보셔도 되고, 준비가 되셨으면 바로 온라인 접수하셔도 됩니다.')}</p>
      <div class="cta">
        <a class="btn gold" id="kakaoBtn" href="#" rel="noopener">{T('KakaoTalk-оор зөвлөгөө авах','카카오톡으로 상담하기')}</a>
        <a class="btn ghost onnavy" href="apply.html">{T('Онлайн бүртгэл','온라인 접수')}</a>
      </div>
      <p class="note" id="kakaoNote" hidden style="color:rgba(255,255,255,.7);margin-top:8px">{T('KakaoTalk холбоос бэлтгэгдэж байна. Одоогоор утсаар холбогдоно уу.','카카오톡 상담 연결은 준비 중입니다. 지금은 전화로 문의해 주세요.')}</p>
      <div class="tel">{T('Утас','전화')} <b>02-536-1260</b><button type="button" class="copy" data-copy="02-536-1260">{T('Хуулах','복사')}</button><br>{T('Ажлын өдөр 09:00–18:00 · 세무법인 위드택스','평일 09:00–18:00 · 세무법인 위드택스')}</div>
    </div>
  </div>
</section>
'''
    js = r'''
  const kb=document.getElementById('kakaoBtn'),kn=document.getElementById('kakaoNote');
  const kurl=window.WITHTAX_KAKAO_URL||'';
  if(kurl){kb.href=kurl;kb.target='_blank';}else{kb.href='#contact';kb.setAttribute('aria-disabled','true');kb.classList.remove('gold');kb.classList.add('ghost','onnavy');kn.hidden=false;kb.addEventListener('click',e=>e.preventDefault());}
  document.querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',()=>{const v=b.dataset.copy;const o=b.innerHTML;const done=()=>{b.textContent=L()==='ko'?'복사됨':'Хуулагдлаа';setTimeout(()=>b.innerHTML=o,1500);};
    if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(v).then(done).catch(()=>{});}));
'''
    return shell('박경준 세무사의 외국인 경정청구 — 세무법인 위드택스', body, '', js, 'index')

# ============================== CALC ==============================
CALC_CSS = r"""
.page{max-width:760px;margin:0 auto;padding:32px 20px 72px}
.page-h h1{font-family:var(--f-disp);font-size:28px;font-weight:700}
.page-h p{margin-top:8px;color:var(--ink-2)}
.form{display:flex;flex-direction:column;gap:18px;margin-top:22px}
.paytools{display:flex;flex-wrap:wrap;gap:8px 12px;align-items:center}
.paytools .won{flex:1 1 180px}
.chk{display:inline-flex;align-items:center;gap:8px;font-size:15px;cursor:pointer;min-height:44px}
.chk input{accent-color:var(--brand);width:18px;height:18px;margin:0}
.years{display:grid;grid-template-columns:repeat(5,1fr);gap:6px}
.years .y{display:flex;flex-direction:column;gap:3px;min-width:0}
.years .y small{font-size:13px;color:var(--ink-3);font-weight:600}
.years .y input{padding:8px!important;font-size:15px;text-align:right;min-height:44px}
@media (max-width:460px){.years{grid-template-columns:repeat(3,1fr)}}
.extra{border:1px dashed var(--line);border-radius:12px;padding:12px 14px}
.extra summary{cursor:pointer;font-weight:600;font-size:16px;list-style:none;display:flex;justify-content:space-between;gap:8px;min-height:32px;align-items:center}
.extra summary::-webkit-details-marker{display:none}
.extra summary::after{content:"+";color:var(--ink-3);font-size:22px}
.extra[open] summary::after{content:"−"}
.result{border:1px solid var(--brand-2);border-radius:14px;overflow:hidden;background:var(--surface)}
.rhead{background:var(--navy);color:#fff;padding:14px 16px}
.rhead .big{font-size:28px;font-weight:700;font-variant-numeric:tabular-nums;line-height:1.2}
.rhead .lbl2{font-size:14px;opacity:.85}
.tblwrap{overflow-x:auto}
.rt{width:100%;border-collapse:collapse;font-size:14.5px;font-variant-numeric:tabular-nums}
.rt th,.rt td{padding:8px 10px;text-align:right;border-bottom:1px solid var(--line);white-space:nowrap}
.rt th:first-child,.rt td:first-child{text-align:left}
.rt th{font-weight:600;color:var(--ink-3);font-size:12.5px;background:var(--ground)}
.rt td.g{color:var(--ok);font-weight:700}.rt td.m{color:var(--ink-3)}
.rt tr.tot td{font-weight:700;background:var(--ground)}
.rsum{padding:12px 16px;display:grid;grid-template-columns:1fr auto;gap:6px 12px;font-size:15.5px;font-variant-numeric:tabular-nums}
.rsum .k{color:var(--ink-2)}.rsum .v{text-align:right;font-weight:600}
.rsum .net{font-size:18px;color:var(--ok);font-weight:700}
.rsum .fam{color:var(--urgent)}
.assume{padding:12px 16px 16px;font-size:14px;color:var(--ink-2);border-top:1px solid var(--line)}
.assume ul{margin:6px 0 0;padding-left:18px}
.verdict{border-radius:10px;padding:12px 14px;font-size:15.5px;display:none;gap:10px;align-items:flex-start}
.verdict.show{display:flex}
.verdict.good{background:var(--ok-soft);border:1px solid var(--ok)}
.verdict.plain{background:var(--brand-soft);border:1px solid var(--brand-2)}
.verdict.no{background:var(--bad-soft);border:1px solid var(--bad)}
.verdict .ic{flex:none;width:26px;height:26px;border-radius:50%;display:grid;place-items:center;font-weight:700;color:#fff}
.verdict.good .ic{background:var(--ok)}.verdict.plain .ic{background:var(--brand-2)}.verdict.no .ic{background:var(--bad)}
"""

def CALC():
    body = f'''
<main class="page">
  <div class="page-h">
    <h1>{T('Урьдчилсан буцаалтын тооцоо','예상 환급액 계산')}</h1>
    <p>{T('Урьдчилсан тооцоо үнэгүй. Хувийн мэдээлэл оруулахгүй. Тооцоолсны дараа бүртгүүлэх эсэхээ шийднэ үү.','예상액 계산은 무료이며 개인정보를 입력하지 않습니다. 계산 후 신청 여부를 결정하세요.')}</p>
  </div>
  <div class="form">
    <div class="grid2">
      <div class="field">
        <label for="hireYM">{T('Солонгост анх ажилд орсон он, сар','한국 최초 취업 연월')}</label>
        <input id="hireYM" inputmode="numeric" maxlength="7" data-ph-mn="201903 → 2019-03" data-ph-ko="201903 → 2019-03">
      </div>
      <div class="field">
        <label for="hireAge">{T('Тэр үеийн нас','취업 당시 나이(만)')}</label>
        <input id="hireAge" inputmode="numeric" maxlength="2" data-ph-mn="25" data-ph-ko="25">
      </div>
    </div>
    <div class="field">
      <div class="lbl">{T('Компанийн салбар','근무 회사 업종')}</div>
      <div class="seg" id="industry">
        <label><input type="radio" name="ind" value="ok">{T('Үйлдвэрлэл','제조업')}</label>
        <label><input type="radio" name="ind" value="ok">{T('Барилга','건설업')}</label>
        <label><input type="radio" name="ind" value="ok">{T('Хөдөө аж ахуй · загас','농업·어업')}</label>
        <label><input type="radio" name="ind" value="ok">{T('Худалдаа · тээвэр · хоол','도소매·운수·음식점')}</label>
        <label><input type="radio" name="ind" value="no">{T('Эмнэлэг · санхүү · боловсрол','보건·금융·교육')}</label>
        <label><input type="radio" name="ind" value="unk">{T('Мэдэхгүй','모름')}</label>
      </div>
      <div class="hint">{T('"Мэдэхгүй" гэж сонговол хөнгөлөлтийг тооцоонд оруулахгүй. Салбарыг баримтаар шалгасны дараа тодорхойлно.','"모름"을 선택하면 감면을 계산에 반영하지 않습니다. 업종은 자료 확인 후 판단합니다.')}</div>
    </div>
    <div class="field">
      <label for="pay">{T('Жилийн нийт цалин (татвар суутгахын өмнөх)','연간 총급여 (세전, 상여 포함)')}</label>
      <div class="won"><input id="pay" inputmode="numeric" data-ph-mn="30,000,000" data-ph-ko="30,000,000"><span>₩</span></div>
      <div class="paytools">
        <span class="hint">{T('Сарын цалин × 12 =','월급 × 12 =')}</span>
        <div class="won"><input id="monthly" inputmode="numeric" data-ph-mn="2,500,000" data-ph-ko="2,500,000"><span>₩/{T('сар','월')}</span></div>
        <label class="chk"><input type="checkbox" id="perYear">{T('Жил бүр өөр','연도별로 다름')}</label>
      </div>
      <div class="years" id="payYears" hidden></div>
    </div>
    <details class="extra" id="extra">
      <summary>{T('Нэмэлт хөнгөлөлт (гэр бүл) — баримт шаардана','추가 공제 (가족) — 서류 필요')}</summary>
      <div class="grid2" style="margin-top:10px">
        <div class="field"><label for="spouse">{T('Эхнэр / нөхөр (орлогогүй)','배우자 (소득 없음)')}</label>
          <select id="spouse"><option value="0" data-mn="Үгүй" data-ko="무">Үгүй</option><option value="1" data-mn="Тийм" data-ko="유">Тийм</option></select></div>
        <div class="field"><label for="kids">{T('Хүүхэд (20 хүртэл)','자녀 (20세 이하)')}</label>
          <select id="kids"><option>0</option><option>1</option><option>2</option><option>3</option><option>4</option></select></div>
      </div>
      <div class="hint">{T('Монголын гэр бүлийн гэрчилгээ, орчуулга, нотариат шаардлагатай. Үр дүнд тусад нь харуулна.','몽골 가족관계증명서와 번역·공증이 필요합니다. 결과에 별도로 표시됩니다.')}</div>
    </details>
    <div class="err" id="cerr" role="alert"></div>
    <div class="verdict" id="verdict"><div class="ic" id="vIc"></div><div><div id="vT"></div><div class="hint" id="vY"></div></div></div>
    <div class="result" id="result" hidden>
      <div class="rhead" id="rhead"></div>
      <div class="tblwrap"><table class="rt" id="rt"></table></div>
      <div class="rsum" id="rsum"></div>
      <div class="assume" id="assume"></div>
    </div>
    <div id="after" hidden style="display:flex;gap:10px;flex-wrap:wrap">
      <a class="btn gold" href="apply.html">{T('Баримт шалгуулахаар бүртгүүлэх','자료 검토 신청하기')}</a>
      <a class="btn ghost" href="index.html#contact">{T('Эхлээд зөвлөгөө авах','먼저 상담하기')}</a>
    </div>
  </div>
</main>
'''
    js = r'''
  const fmt0=n=>Math.round(n).toLocaleString('ko-KR');
  const num=el=>parseInt((el.value||'').replace(/\D/g,''),10)||0;
  function money(el){el.addEventListener('input',()=>{const v=el.value.replace(/\D/g,'').slice(0,10);el.value=v?parseInt(v,10).toLocaleString('ko-KR'):'';});}
  const pay=document.getElementById('pay'),monthly=document.getElementById('monthly'),perYear=document.getElementById('perYear'),payYears=document.getElementById('payYears');
  money(pay);money(monthly);
  monthly.addEventListener('input',()=>{const m=num(monthly);if(m){pay.value=(m*12).toLocaleString('ko-KR');syncYears();}calc();});
  pay.addEventListener('input',()=>{syncYears();calc();});
  Y.forEach(y=>{const d=document.createElement('div');d.className='y';d.innerHTML=`<small>${y}</small><input id="py${y}" inputmode="numeric" aria-label="${y}" placeholder="0">`;payYears.appendChild(d);const i=d.querySelector('input');money(i);i.addEventListener('input',calc);});
  function syncYears(){if(!perYear.checked)Y.forEach(y=>{document.getElementById('py'+y).value=pay.value;});}
  perYear.addEventListener('change',()=>{payYears.hidden=!perYear.checked;syncYears();calc();});
  const hym=document.getElementById('hireYM');
  hym.addEventListener('input',()=>{const v=hym.value.replace(/\D/g,'').slice(0,6);hym.value=v.length>4?v.slice(0,4)+'-'+v.slice(4):v;});
''' + TAXCORE + r'''
  const vb=document.getElementById('verdict'),vIc=document.getElementById('vIc'),vT=document.getElementById('vT'),vY=document.getElementById('vY');
  const result=document.getElementById('result'),after=document.getElementById('after'),cerr=document.getElementById('cerr');
  function verdict(cls,ic,mn,ko,yrs){vb.className='verdict show '+cls;vIc.textContent=ic;vT.textContent=L()==='ko'?ko:mn;vY.textContent=yrs||'';}
  function calc(){
    const ko=L()==='ko';
    const ym=hym.value, ageRaw=document.getElementById('hireAge').value, age=parseInt(ageRaw,10);
    const ind=(document.querySelector('input[name=ind]:checked')||{}).value;
    cerr.textContent='';
    if(ym&&!/^\d{4}-\d{2}$/.test(ym)){cerr.textContent=ko?'취업 연월은 2019-03 형식으로 입력하세요.':'Он сарыг 2019-03 хэлбэрээр оруулна уу.';}
    else if(ym){const yy=+ym.slice(0,4),mm=+ym.slice(5,7);if(yy<2000||yy>2026||mm<1||mm>12)cerr.textContent=ko?'취업 연월이 올바르지 않습니다.':'Он сар буруу байна.';}
    if(ageRaw&&(isNaN(age)||age<15||age>70))cerr.textContent=ko?'나이는 15~70 사이로 입력하세요.':'Насыг 15–70 хооронд оруулна уу.';
    if(!/^\d{4}-\d{2}$/.test(ym)||isNaN(age)||!ind||cerr.textContent){vb.className='verdict';result.hidden=true;after.hidden=true;return;}
    const hy=+ym.slice(0,4), hm=+ym.slice(5,7);
    let reason=null, relief=true;
    if(age>34){relief=false;reason=['Ажилд орох үед 34-өөс дээш настай тул хөнгөлөлт хамаарахгүй. Зардлын хасалтаар л шалгана.','취업 당시 34세 초과로 감면 대상이 아닙니다. 공제자료 반영분만 검토합니다.'];}
    else if(ind==='no'){relief=false;reason=['Энэ салбар хөнгөлөлтөд хамаарахгүй. Зардлын хасалтаар л шалгана.','선택한 업종은 감면 제외 업종입니다. 공제자료 반영분만 검토합니다.'];}
    else if(ind==='unk'){relief=false;reason=['Салбар тодорхойгүй тул хөнгөлөлтийг тооцоонд оруулаагүй. Баримт шалгасны дараа тодорхойлно.','업종이 확인되지 않아 감면을 계산에 반영하지 않았습니다. 자료 확인 후 판단합니다.'];}
    else if(hy+5<2021){relief=false;reason=['Хөнгөлөлтийн 5 жил 2021 оноос өмнө дууссан.','감면 5년이 2021년 이전에 끝났습니다.'];}
    const ratio={};Y.forEach(y=>{let r=0;if(relief){if(y>=hy&&y<hy+5)r=1;else if(y===hy+5)r=hm/12;if(y<2018)r=0;}ratio[y]=r;});
    const spouse=+document.getElementById('spouse').value, kids=+document.getElementById('kids').value, extra=(spouse+kids)*1.5e6;
    let rows=[],tot=0,famTot=0,anyPay=false;
    Y.forEach(y=>{if(y<hy)return;const g=perYear.checked?num(document.getElementById('py'+y)):num(pay);if(!g)return;anyPay=true;
      const base=yearTax(g,y,0,0), w=yearTax(g,y,0,ratio[y]), f=yearTax(g,y,extra,ratio[y]);
      const ref=Math.max(0,base.tax-w.tax), fam=Math.max(0,w.tax-f.tax);
      tot+=ref;famTot+=fam;rows.push({y,g,base:base.tax,w:w.tax,ref,fam,r:ratio[y]});});
    if(!anyPay){result.hidden=true;after.hidden=true;
      if(reason)verdict('plain','i',reason[0],reason[1]);
      else verdict('good','✓','Оруулсан мэдээллээр хөнгөлөлт авах боломжтой байж болзошгүй. Баримт шалгасны дараа тодорхойлно. Цалингаа оруулбал дүнг харуулна.','입력 정보상 감면 가능성이 있습니다. 서류 확인 후 확정됩니다. 연봉을 입력하면 금액이 나옵니다.');
      return;}
    vb.className='verdict';
    const local=tot*.1, gross=tot+local, fee=Math.round(gross*.22), net=gross-fee;
    document.getElementById('rhead').innerHTML=`<div class="lbl2">${ko?'예상 환급액 (지방소득세 포함, 수수료 차감 전)':'Урьдчилсан буцаалт (орон нутгийн татвар орсон, хураамж хасахаас өмнө)'}</div><div class="big">${fmt0(gross)} ₩</div>`;
    const th=ko?['귀속','총급여','감면 미적용 가정 추정세액','감면 적용 시','예상 환급']:['Он','Цалин','Хөнгөлөлтгүй тооцсон татвар','Хөнгөлөлттэй','Буцаалт'];
    let html='<tr>'+th.map(t=>`<th>${t}</th>`).join('')+'</tr>';
    rows.forEach(r=>{html+=`<tr><td>${r.y}${r.r>0&&r.r<1?` <span class="m">(${Math.round(r.r*12)}${ko?'개월':' сар'})</span>`:''}</td><td class="m">${fmt0(r.g)}</td><td>${fmt0(r.base)}</td><td>${r.r?fmt0(r.w):'<span class="m">—</span>'}</td><td class="${r.ref>0?'g':'m'}">${r.ref>0?'+'+fmt0(r.ref):'0'}</td></tr>`;});
    html+=`<tr class="tot"><td colspan="4">${ko?'합계 (국세)':'Нийт (улсын татвар)'}</td><td class="g">${fmt0(tot)}</td></tr>`;
    document.getElementById('rt').innerHTML=html;
    let sum=`<span class="k">${ko?'예상 환급액 (국세 + 지방소득세 10%)':'Урьдчилсан буцаалт (улсын + орон нутгийн 10%)'}</span><span class="v">${fmt0(gross)}</span>
      <span class="k">${ko?'수수료 22% (부가세 포함)':'Хураамж 22% (НӨАТ орсон)'}</span><span class="v">−${fmt0(fee)}</span>
      <span class="k net">${ko?'수수료 차감 후 예상 수령액':'Хураамж хассаны дараа таны гарт'}</span><span class="v net">${fmt0(net)} ₩</span>`;
    if(extra>0)sum+=`<span class="k fam">${ko?'가족 공제 추가 예상액 (서류 제출 시, 수수료 차감 전)':'Гэр бүлийн хөнгөлөлтийн нэмэлт (баримт өгвөл, хураамж хасахаас өмнө)'}</span><span class="v fam">+${fmt0(famTot*1.1)}</span>`;
    document.getElementById('rsum').innerHTML=sum;
    const A=ko?['<b>계산 가정과 한계</b>','추정치입니다. 실제 환급액은 원천징수영수증 등 자료를 기준으로 재계산됩니다.','근로소득공제, 본인 기본공제, 표준세액공제만 가정했습니다. 국민연금·건강보험 공제는 반영하지 않았습니다.','회사 연말정산에서 이미 감면·공제를 적용받은 연도는 환급액이 줄거나 없을 수 있습니다.','실제 납부세액을 입력받지 않았으므로 "추정세액"으로 표시합니다.','2020년 이전분은 계산에서 제외했습니다.']:['<b>Тооцооны таамаглал ба хязгаар</b>','Урьдчилсан дүн. Бодит буцаалт нь цалингийн татварын тодорхойлолт зэрэг баримтаар дахин тооцогдоно.','Зөвхөн цалингийн орлогын хасалт, өөрийн суурь хасалт, стандарт татварын хөнгөлөлтийг тооцсон. Тэтгэвэр, эрүүл мэндийн даатгалын хасалтыг оруулаагүй.','Компани жилийн эцсийн тооцоонд хөнгөлөлт, хасалтыг аль хэдийн хэрэглэсэн жилд буцаалт багасах эсвэл гарахгүй байж болно.','Бодит төлсөн татварыг оруулаагүй тул "тооцсон татвар" гэж харуулав.','2020 ба өмнөх оныг тооцооноос хассан.'];
    document.getElementById('assume').innerHTML=A[0]+'<ul>'+A.slice(1).map(x=>'<li>'+x+'</li>').join('')+'</ul>'+(reason?'<p style="margin-top:8px">'+(ko?reason[1]:reason[0])+'</p>':'');
    result.hidden=false;after.hidden=false;
  }
  ['hireYM','hireAge','spouse','kids'].forEach(id=>document.getElementById(id).addEventListener('input',calc));
  document.getElementById('industry').addEventListener('change',calc);
  function onLang(){calc();}
'''
    return shell('예상 환급액 계산 — 세무법인 위드택스', body, '', js, 'calc')

# ============================== APPLY ==============================
APPLY_CSS = r"""
.page{max-width:760px;margin:0 auto;padding:32px 20px 72px}
.page-h h1{font-family:var(--f-disp);font-size:28px;font-weight:700}
.page-h p{margin-top:8px;color:var(--ink-2)}
.stepbar{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin:22px 0 18px;counter-reset:st}
.stepbar div{counter-increment:st;font-size:14px;color:var(--ink-3);padding-top:10px;border-top:4px solid var(--line);min-width:0;word-break:keep-all;overflow-wrap:break-word}
.stepbar div::before{content:counter(st) ". ";font-weight:700}
.stepbar div.cur{color:var(--navy);border-top-color:var(--gold);font-weight:700}
.stepbar div.done{border-top-color:var(--ok);color:var(--ok)}
.form{display:flex;flex-direction:column;gap:18px}
.form h2{font-size:20px}
.form h3{font-size:16px;color:var(--brand);margin-top:4px}
.form hr{border:0;border-top:1px dashed var(--line);margin:4px 0}
.navrow{display:flex;gap:10px;flex-wrap:wrap;margin-top:8px}
.navrow .btn{flex:1 1 160px}
.slots{display:flex;flex-direction:column;gap:12px}
.slot{border:1px solid var(--line);border-radius:12px;padding:14px;background:var(--surface)}
.slot.ok{border-color:var(--ok)}
.slot.over{border-color:var(--brand);background:var(--brand-soft);border-style:dashed}
.slot-h{display:flex;justify-content:space-between;gap:8px;font-weight:600;font-size:16px;margin-bottom:4px}
.slot-h .t{flex:1;min-width:0}
.slot-sub{font-size:14px;color:var(--ink-3);margin-bottom:10px}
.slot-b{display:flex;flex-wrap:wrap;gap:8px}
label.file{display:inline-flex;align-items:center;gap:6px;border:1px dashed var(--brand-2);color:var(--brand);border-radius:10px;padding:10px 14px;font-size:15px;font-weight:600;cursor:pointer;background:var(--surface);position:relative;min-height:48px}
label.file.cam{border-style:solid;background:var(--brand-soft)}
label.file input{position:absolute;width:1px;height:1px;opacity:0;pointer-events:none}
.dz{font-size:13px;color:var(--ink-3);margin-top:6px}
@media (hover:none){.dz{display:none}}
.flist{list-style:none;margin:8px 0 0;padding:0;display:flex;flex-direction:column;gap:4px}
.flist:empty{display:none}
.flist li{display:flex;align-items:center;gap:8px;font-size:14.5px;background:var(--ground);border-radius:8px;padding:6px 10px;min-width:0}
.flist li img{width:36px;height:36px;object-fit:cover;border-radius:5px;flex:none}
.flist li .pdf{width:36px;height:36px;border-radius:5px;background:var(--bad-soft);color:var(--bad);font-size:11px;font-weight:700;display:grid;place-items:center;flex:none}
.flist li .nm{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.flist li .sz{color:var(--ink-3);font-variant-numeric:tabular-nums;flex:none;font-size:13px}
.flist li button{border:0;background:transparent;color:var(--ink-2);font-size:20px;cursor:pointer;width:40px;height:40px;flex:none;border-radius:8px}
.flist li button:hover{background:var(--bad-soft);color:var(--bad)}
.prog{display:flex;flex-direction:column;gap:8px;font-size:16px;color:var(--ink-2);padding:16px;border-radius:10px;background:var(--brand-soft)}
.prog-h{display:flex;justify-content:space-between;align-items:baseline;gap:12px}
.prog-h b{font-size:22px;color:var(--navy);font-variant-numeric:tabular-nums;flex:none}
.prog .bar{height:14px;border-radius:7px;background:#fff;border:1px solid var(--line);overflow:hidden}
.prog .bar i{display:block;height:100%;width:0;background:var(--navy);transition:width .3s}
.prog-hint{font-size:14px;color:var(--ink-3)}
.summary{display:grid;grid-template-columns:auto 1fr;gap:8px 14px;font-size:15px;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:14px}
.summary dt{color:var(--ink-3)}.summary dd{margin:0;min-width:0;overflow-wrap:anywhere}
.agree{display:flex;gap:12px;align-items:flex-start;font-size:15.5px;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px 14px}
.agree input{width:22px;height:22px;margin-top:2px;accent-color:var(--brand);flex:none}
.agree details{font-size:14px;color:var(--ink-3);margin-top:6px}
.agree summary{cursor:pointer;min-height:28px}
.done{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:26px 20px}
.done .ok{width:52px;height:52px;border-radius:50%;background:var(--ok-soft);color:var(--ok);display:grid;place-items:center;margin:0 auto 10px;font-size:26px;font-weight:700}
.done h2{font-size:21px;text-align:center}
.done p{margin-top:6px;color:var(--ink-2);text-align:center}
.pw{background:var(--urgent-soft);border-radius:12px;padding:14px;display:flex;flex-direction:column;gap:10px}
.pwrow{position:relative}
.pwrow button{position:absolute;right:6px;top:50%;transform:translateY(-50%);font:inherit;font-size:13px;border:0;background:var(--ground);color:var(--ink-2);border-radius:8px;padding:8px 10px;cursor:pointer;min-height:36px}
.proxy{display:flex;gap:12px;align-items:flex-start;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px 14px;font-size:15.5px}
.proxy input{width:22px;height:22px;accent-color:var(--brand);margin-top:2px;flex:none}
.proxy>div{flex:1;min-width:0}
#proxyFields{margin-top:10px}
"""

def slot(role, mn, ko, sub_mn, sub_ko, req=False, multi=False, cam=True, pdf_only=False):
    acc = 'application/pdf' if pdf_only else 'image/*,application/pdf'
    camb = '' if not cam else f'<label class="file cam"><input type="file" accept="image/*" capture="environment"><span aria-hidden="true">📷</span>{T("Зураг авах","사진 촬영")}</label>'
    return f'''      <div class="slot" data-role="{role}"{' data-req="1"' if req else ''}{' data-multi="1"' if multi else ''}>
        <div class="slot-h">{T(mn,ko)}{'<span class="req-tag" style="color:var(--bad)" aria-label="필수">*</span>' if req else f'<span class="note">{T("сонголттой","선택")}</span>'}</div>
        <div class="slot-sub">{T(sub_mn,sub_ko)}</div>
        <div class="slot-b">{camb}<label class="file"><input type="file" accept="{acc}"{' multiple' if multi else ''}><span aria-hidden="true">＋</span>{T('Файл сонгох'+(' (олон)' if multi else ''),'파일 선택'+(' (여러 개)' if multi else ''))}</label></div>
        <div class="dz">{T('эсвэл файлаа энд чирж тавина / Ctrl+V','또는 여기에 파일을 끌어다 놓기 / Ctrl+V 붙여넣기')}</div>
        <ul class="flist"></ul>
      </div>
'''

def APPLY():
    body = f'''
<main class="page">
  <div class="page-h">
    <h1>{T('Онлайн бүртгэл','온라인 접수')}</h1>
    <p>{T('Гурван алхамаар бөглөнө. Өмнөх алхам руу буцсан ч оруулсан мэдээлэл, файл хадгалагдана.','3단계로 작성합니다. 이전 단계로 돌아가도 입력한 내용과 첨부파일은 유지됩니다.')}</p>
  </div>
  <div class="callout" id="offline" hidden>{T('Онлайн бүртгэл одоогоор бэлтгэгдэж байна. Утсаар (02-536-1260) эсвэл хариуцагчтай холбогдоно уу.','온라인 접수 기능은 현재 준비 중입니다. 전화(02-536-1260) 또는 담당자에게 문의해 주세요.')}</div>
  <div class="stepbar" aria-label="진행 단계"><div id="sb1" class="cur">{T('Үндсэн мэдээлэл','기본정보')}</div><div id="sb2">{T('Ажлын түүх ба баримт','근무 이력과 자료 제출')}</div><div id="sb3">{T('Шалгалт ба зөвшөөрөл','최종 확인과 동의')}</div></div>

  <form class="form" id="apply" novalidate>
    <!-- STEP 1 -->
    <section id="s1">
      <div class="form">
        <h2>{T('1. Үндсэн мэдээлэл','1. 기본정보')}</h2>
        <div class="proxy"><input type="checkbox" id="proxy"><div><label for="proxy">{T('Хариуцагч ажилтны өмнөөс оруулж байна','담당자가 근로자 대신 입력')}</label>
          <div id="proxyFields" hidden><div class="grid2">
            <div class="field"><label for="pxName">{T('Хариуцагчийн нэр','담당자 이름')}</label><input id="pxName" autocomplete="off"></div>
            <div class="field"><label for="pxTel">{T('Хариуцагчийн утас','담당자 연락처')}</label><input id="pxTel" inputmode="tel" data-ph-mn="010-0000-0000" data-ph-ko="010-0000-0000"></div>
          </div></div></div></div>
        <div class="field"><label for="name" class="req">{T('Овог нэр — гадаад иргэний үнэмлэх дээрх латин үсгээр','영문 성명 — 외국인등록증과 똑같이')}</label><input id="name" autocomplete="name" data-ph-mn="GERELKHUU ARIUNBOLD" data-ph-ko="GERELKHUU ARIUNBOLD" style="text-transform:uppercase"></div>
        <div class="grid2">
          <div class="field"><label for="phone" class="req">{T('Гар утас','휴대폰')}</label><input id="phone" inputmode="tel" autocomplete="tel" data-ph-mn="010-0000-0000" data-ph-ko="010-0000-0000"></div>
          <div class="field"><label for="visa">{T('Визний төрөл','체류자격')}</label><select id="visa"><option value="" data-mn="—" data-ko="—">—</option><option>E-9</option><option>E-7</option><option>F-2</option><option>F-4</option><option>F-6</option><option value="other" data-mn="Бусад" data-ko="기타">Бусад</option></select></div>
        </div>
        <div class="field"><label for="hireDate" class="req">{T('Солонгост анх ажилд орсон огноо','한국 최초 취업일')}</label><input id="hireDate" inputmode="numeric" maxlength="10" data-ph-mn="20190326 → 2019-03-26" data-ph-ko="20190326 → 2019-03-26"><div class="hint">{T('Хөдөлмөрийн гэрээний огноо. Мэдэхгүй бол ойролцоогоор.','근로계약일 기준. 정확히 모르면 대략적으로.')}</div></div>
        <div class="err" id="err1" role="alert"></div>
        <div class="navrow"><button type="button" class="btn navy" data-go="2">{T('Дараах','다음')}</button></div>
      </div>
    </section>

    <!-- STEP 2 -->
    <section id="s2" hidden>
      <div class="form">
        <h2>{T('2. Ажлын түүх ба баримт','2. 근무 이력과 자료 제출')}</h2>
        <div class="grid2">
          <div class="field"><label for="arc" class="req">{T('Гадаад иргэний бүртгэлийн дугаар','외국인등록번호')}</label><input id="arc" inputmode="numeric" maxlength="14" data-ph-mn="990430-5000000" data-ph-ko="990430-5000000"></div>
          <div class="field"><label for="arcOld">{T('Өмнөх дугаар (виз солигдсон бол)','이전 외국인등록번호 (체류자격 변경 시)')}</label><input id="arcOld" inputmode="numeric" maxlength="14"></div>
        </div>
        <div class="field"><label for="addr" class="req">{T('Одоогийн хаяг (Солонгос)','현재 주소 (한국)')}</label><input id="addr" autocomplete="street-address" data-ph-mn="경기도 ○○시 ○○로 00, 000호" data-ph-ko="경기도 ○○시 ○○로 00, 000호"></div>
        <div class="field"><label for="companies">{T('Ажилласан компаниуд (он, нэр)','근무 회사 (연도, 회사명)')}</label><textarea id="companies" data-ph-mn="2021~2023 (주)광축&#10;2024~ 유일테크" data-ph-ko="2021~2023 (주)광축&#10;2024~ 유일테크"></textarea></div>
        <div class="field"><div class="lbl req">{T('Өмнө нь татварын буцаалт авч байсан уу?','이전에 환급 받은 적 있습니까?')}</div>
          <div class="seg three"><label><input type="radio" name="prev" value="no">{T('Үгүй','없음')}</label><label><input type="radio" name="prev" value="yes">{T('Тийм','있음')}</label><label><input type="radio" name="prev" value="unk">{T('Мэдэхгүй','모름')}</label></div>
          <input id="prevYears" hidden data-ph-mn="2024 оныг хүртэл" data-ph-ko="2024년까지"></div>
        <hr>
        <h3>{T('Баримт хавсаргах','자료 첨부')}</h3>
        <div class="callout info">{T('Файлын төрөл: JPG, PNG, PDF. Нэг файл 10MB хүртэл. Зургийг автоматаар багасгаж илгээнэ. Утсаар бол "Зураг авах" дарж шууд зургаа авна.','첨부 가능: JPG·PNG·PDF, 파일당 10MB까지. 사진은 자동으로 축소되어 전송됩니다. 휴대폰에서는 "사진 촬영"으로 바로 찍을 수 있습니다.')}</div>
        <div class="slots">
{slot('id_front','Гадаад иргэний үнэмлэх — урд тал','외국인등록증 앞면','Тод, бүтэн харагдахаар','글자가 잘 보이게 전체가 나오도록',req=True)}
{slot('id_back','Гадаад иргэний үнэмлэх — ар тал','외국인등록증 뒷면','','',req=True)}
{slot('id_old','Хуучин үнэмлэх','변경 전 등록증','Виз солигдсон бол','체류자격이 바뀐 경우만')}
{slot('simplified','Жилийн эцсийн тооцооны баримт PDF (연말정산 간소화자료)','연말정산 간소화자료 PDF','Хоумтаксаас татсан он тус бүрийн PDF. Байхгүй бол хариуцагч тусална.','홈택스에서 내려받은 연도별 PDF. 없으면 담당자가 안내합니다.',multi=True,cam=False,pdf_only=True)}
{slot('withholding','Цалингийн татварын тодорхойлолт (원천징수영수증)','근로소득 원천징수영수증','Компаниас авсан он тус бүрийн баримт. Зураг эсвэл PDF.','회사에서 받은 연도별 서류. 사진 또는 PDF.',multi=True)}
{slot('other','Бусад','기타','Цалингийн хуудас, гэрээ г.м.','급여명세서·근로계약서 등',multi=True)}
        </div>
        <hr>
        <h3>{T('Хоумтакс (홈택스) нэвтрэх мэдээлэл','홈택스 로그인 정보')}</h3>
        <div class="pw">
          <div class="hint" style="color:var(--ink)">{T('Жилийн эцсийн тооцооны баримтыг таны бүртгэлээр авахад ашиглана. Мэдэхгүй бол хоосон орхино уу — хариуцагч тусад нь зааварлана. Ажил дууссаны дараа нууц үгээ солихыг зөвлөж байна.','연말정산 간소화자료 조회에만 사용합니다. 모르면 비워두세요 — 담당자가 별도로 안내합니다. 작업 완료 후 비밀번호 변경을 권장합니다.')}</div>
          <div class="grid2">
            <div class="field"><label for="htId">{T('Хоумтакс ID','홈택스 아이디')}</label><input id="htId" autocomplete="off"></div>
            <div class="field"><label for="htPw">{T('Нууц үг','비밀번호')}</label><div class="pwrow"><input id="htPw" type="password" autocomplete="off"><button type="button" id="pwEye">{T('Харах','보기')}</button></div></div>
          </div>
        </div>
        <div class="err" id="err2" role="alert"></div>
        <div class="navrow"><button type="button" class="btn ghost" data-go="1">{T('Өмнөх','이전')}</button><button type="button" class="btn navy" data-go="3">{T('Дараах','다음')}</button></div>
      </div>
    </section>

    <!-- STEP 3 -->
    <section id="s3" hidden>
      <div class="form">
        <h2>{T('3. Шалгалт ба зөвшөөрөл','3. 최종 확인과 동의')}</h2>
        <div class="field"><div class="lbl req">{T('Буцаалт хүлээн авах өөрийн нэр дээрх данс','환급받을 본인 명의 계좌를 입력해 주세요.')}</div>
          <div class="grid2"><select id="bank" aria-label="은행"><option value="" data-mn="Банк" data-ko="은행">Банк</option><option>국민은행</option><option>신한은행</option><option>우리은행</option><option>하나은행</option><option>농협</option><option>기업은행</option><option>카카오뱅크</option><option>토스뱅크</option><option value="other" data-mn="Бусад" data-ko="기타">Бусад</option></select><input id="acct" inputmode="numeric" aria-label="계좌번호" data-ph-mn="Дансны дугаар" data-ph-ko="계좌번호"></div>
          <div class="hint">{T('Татварын алба өөр хүний данс руу шилжүүлдэггүй.','국세청은 타인 명의 계좌로 환급하지 않습니다.')}</div></div>
        <div class="field"><label for="memo">{T('Нэмэлт тайлбар','추가 메모')}</label><textarea id="memo"></textarea></div>
        <h3>{T('Оруулсан мэдээлэл','입력 내용 확인')}</h3>
        <dl class="summary" id="review"></dl>
        <div class="agree"><input type="checkbox" id="agree1"><div><label for="agree1"><b>{T('[Заавал]','[필수]')}</b> {T('Хувийн мэдээлэл цуглуулж, ашиглахыг зөвшөөрч байна.','개인정보 수집·이용에 동의합니다.')}</label>
          <details><summary>{T('Дэлгэрэнгүй','내용 보기')}</summary>{T('Цуглуулах: нэр, бүртгэлийн дугаар, утас, хаяг, ажлын түүх, данс, Хоумтакс нэвтрэх мэдээлэл, хавсаргасан баримт · Зорилго: татварын буцаалтын шалгалт, мэдүүлэг, үр дүн мэдэгдэх · Хадгалах хугацаа: компанийн журмын дагуу (тусад нь мэдэгдэнэ) · Татгалзвал бүртгэл боломжгүй.','수집 항목: 성명, 외국인등록번호, 연락처, 주소, 근무이력, 계좌, 홈택스 로그인정보, 첨부서류 · 목적: 근로소득세 환급 검토·신고 대행·결과 안내 · 보관기간: 회사 운영정책에 따름(별도 안내) · 거부 시 접수 불가.')}</details></div></div>
        <div class="agree"><input type="checkbox" id="agree2"><div><label for="agree2"><b>{T('[Заавал]','[필수]')}</b> {T('Татварын төлөөлөгчөөр 세무법인 위드택스-ийг томилохыг зөвшөөрч байна (мэдүүлэг гаргахын өмнө дахин баталгаажуулна).','세무대리인으로 세무법인 위드택스를 선임하는 데 동의합니다 (실제 신고 전 다시 확인합니다).')}</label></div></div>
        <div class="err" id="err3" role="alert"></div>
        <button class="btn gold block" type="submit" id="submitBtn">{T('Бүртгүүлэх','접수하기')}</button>
        <div class="prog" id="prog" hidden><div class="prog-h"><span id="progT"></span><b id="progP">0%</b></div><div class="bar"><i id="bar"></i></div><span class="prog-hint">{T('Илгээж дуустал хуудсыг хаахгүй байна уу.','전송이 끝날 때까지 화면을 닫지 마세요.')}</span></div>
        <div class="navrow"><button type="button" class="btn ghost" data-go="2">{T('Өмнөх','이전')}</button></div>
        <p class="note">{T('Бүртгэлийн дараа хариуцагч баримтыг шалгаад холбогдоно.','접수 후 담당자가 자료를 확인하고 연락드립니다.')}</p>
      </div>
    </section>
  </form>

  <section class="done" id="done" hidden>
    <div class="ok" aria-hidden="true">✓</div>
    <h2>{T('Бүртгэл хүлээн авлаа','접수되었습니다')}</h2>
    <p>{T('Шаардлагатай баримт бүгд баталгаажсанаас хойш 3 ажлын өдрийн дотор шалгалтын үр дүнг мэдэгдэнэ.','필요한 자료가 모두 확인되면 영업일 3일 이내 검토 결과를 안내합니다.')}</p>
    <dl class="summary" id="summary" style="margin-top:16px"></dl>
  </section>
</main>
'''
    js = r'''
  const ENDPOINT=window.WITHTAX_ENDPOINT||'';
  const MAX_FILE=10*1024*1024;
  const store={};
  const $=id=>document.getElementById(id);
  const g=id=>($(id).value||'').trim();
  const fmt=b=>b>1048576?(b/1048576).toFixed(1)+'MB':Math.max(1,Math.round(b/1024))+'KB';
  if(!ENDPOINT){$('offline').hidden=false;$('submitBtn').disabled=true;}
  // ---- steps ----
  let cur=1;
  function show(n){cur=n;[1,2,3].forEach(i=>{$('s'+i).hidden=i!==n;const sb=$('sb'+i);sb.className=i===n?'cur':(i<n?'done':'');});
    if(n===3)renderReview();window.scrollTo({top:0,behavior:'smooth'});}
  function v1(){const ko=L()==='ko';
    if(!g('name'))return [ko?'영문 성명을 입력하세요.':'Овог нэрээ оруулна уу.','name'];
    if(g('phone').replace(/\D/g,'').length<10)return [ko?'휴대폰 번호를 정확히 입력하세요.':'Утасны дугаараа зөв оруулна уу.','phone'];
    const m=g('hireDate').match(/^(\d{4})-(\d{2})-(\d{2})$/);
    if(!m||+m[1]<2000||+m[1]>2026||+m[2]<1||+m[2]>12||+m[3]<1||+m[3]>31)return [ko?'최초 취업일을 2019-03-26 형식으로 입력하세요.':'Ажилд орсон огноог 2019-03-26 хэлбэрээр оруулна уу.','hireDate'];
    return null;}
  function v2(){const ko=L()==='ko';
    if(g('arc').replace(/\D/g,'').length!==13)return [ko?'외국인등록번호 13자리를 입력하세요.':'Бүртгэлийн дугаарын 13 оронг оруулна уу.','arc'];
    if(!g('addr'))return [ko?'주소를 입력하세요.':'Хаягаа оруулна уу.','addr'];
    if(!document.querySelector('input[name=prev]:checked'))return [ko?'이전 환급 여부를 선택하세요.':'Өмнө буцаалт авсан эсэхээ сонгоно уу.',null];
    for(const s of document.querySelectorAll('.slot[data-req]')){if(!store[s.dataset.role].length)return [(ko?'필수 자료 누락: ':'Шаардлагатай баримт дутуу: ')+s.querySelector('.slot-h .'+(ko?'ko':'mn')).textContent,null,s];}
    return null;}
  function v3(){const ko=L()==='ko';
    if(!g('bank'))return [ko?'은행을 선택하세요.':'Банкаа сонгоно уу.','bank'];
    if(g('acct').replace(/\D/g,'').length<6)return [ko?'계좌번호를 입력하세요.':'Дансны дугаараа оруулна уу.','acct'];
    if(!$('agree1').checked||!$('agree2').checked)return [ko?'필수 동의 2가지에 체크해 주세요.':'Заавал 2 зөвшөөрлийг чагтална уу.',null];
    return null;}
  function showErr(n,r){const e=$('err'+n);if(!r){e.textContent='';return true;}e.textContent=r[0];if(r[1])$(r[1]).focus();if(r[2])r[2].scrollIntoView({behavior:'smooth',block:'center'});return false;}
  document.querySelectorAll('[data-go]').forEach(b=>b.addEventListener('click',()=>{const to=+b.dataset.go;
    if(to>cur){if(cur===1&&!showErr(1,v1()))return;if(cur===2&&!showErr(2,v2()))return;}
    show(to);}));
  function renderReview(){const ko=L()==='ko';const files=Object.values(store).reduce((a,l)=>a+l.length,0);
    const rows=[[ko?'성명':'Нэр',g('name').toUpperCase()],[ko?'휴대폰':'Утас',g('phone')],[ko?'최초 취업일':'Ажилд орсон огноо',g('hireDate')],[ko?'외국인등록번호':'Бүртгэлийн дугаар',g('arc').slice(0,8)+'*****'],[ko?'주소':'Хаяг',g('addr')],[ko?'첨부 파일':'Файл',files+(ko?'건':'')],[ko?'홈택스 아이디':'Хоумтакс ID',g('htId')||(ko?'미입력 (담당자 안내)':'Хоосон (хариуцагч зааварлана)')]];
    const dl=$('review');dl.innerHTML='';rows.forEach(([k,v])=>{const dt=document.createElement('dt');dt.textContent=k;const dd=document.createElement('dd');dd.textContent=v;dl.append(dt,dd);});}
  // ---- files ----
  function renderSlot(slot){const role=slot.dataset.role,list=store[role]||[],ul=slot.querySelector('.flist');ul.innerHTML='';const ko=L()==='ko';
    list.forEach((f,i)=>{const li=document.createElement('li');
      if(f.type.startsWith('image/')){const im=document.createElement('img');im.src=URL.createObjectURL(f);im.alt='';li.appendChild(im);}else{const d=document.createElement('span');d.className='pdf';d.textContent='PDF';li.appendChild(d);}
      const nm=document.createElement('span');nm.className='nm';nm.textContent=f.name;const sz=document.createElement('span');sz.className='sz';sz.textContent=fmt(f.size);
      const b=document.createElement('button');b.type='button';b.textContent='×';b.setAttribute('aria-label',(ko?'삭제: ':'Устгах: ')+f.name);b.onclick=()=>{list.splice(i,1);renderSlot(slot);};
      li.append(nm,sz,b);ul.appendChild(li);});
    slot.classList.toggle('ok',list.length>0);}
  function renderAll(){document.querySelectorAll('.slot').forEach(renderSlot);}
  document.querySelectorAll('.slot').forEach(slot=>{
    const role=slot.dataset.role,multi=!!slot.dataset.multi;store[role]=[];
    const accept=role==='simplified'?f=>f.type==='application/pdf':f=>f.type==='application/pdf'||f.type.startsWith('image/');
    const addFiles=list=>{const err=$('err2');const ko=L()==='ko';
      for(const f of list){if(!accept(f)){err.textContent=(ko?'PDF 또는 이미지만 가능: ':'Зөвхөн PDF эсвэл зураг: ')+f.name;continue;}
        if(f.size>MAX_FILE){err.textContent=(ko?'10MB 초과: ':'10MB-аас их: ')+f.name;continue;}
        if(!multi)store[role]=[];if(!store[role].some(x=>x.name===f.name&&x.size===f.size))store[role].push(f);}
      renderSlot(slot);};
    slot.querySelectorAll('input[type=file]').forEach(inp=>inp.addEventListener('change',()=>{addFiles(inp.files);inp.value='';}));
    ['dragenter','dragover'].forEach(ev=>slot.addEventListener(ev,e=>{e.preventDefault();e.stopPropagation();slot.classList.add('over');}));
    ['dragleave','drop'].forEach(ev=>slot.addEventListener(ev,e=>{e.preventDefault();e.stopPropagation();slot.classList.remove('over');}));
    slot.addEventListener('drop',e=>addFiles(e.dataTransfer.files));
    slot.tabIndex=0;
    slot.addEventListener('paste',e=>{const fs=[...(e.clipboardData?.files||[])];if(fs.length){e.preventDefault();addFiles(fs.map((f,i)=>f.name&&f.name!=='image.png'?f:new File([f],'paste_'+Date.now()+'_'+i+'.'+(f.type.split('/')[1]||'png'),{type:f.type})));}});
    slot.addEventListener('click',e=>{if(!e.target.closest('label,button,input'))slot.focus();});
  });
  ['dragover','drop'].forEach(ev=>document.addEventListener(ev,e=>{if(!e.target.closest('.slot'))e.preventDefault();}));
  // ---- inputs ----
  const proxy=$('proxy');proxy.addEventListener('change',()=>{$('proxyFields').hidden=!proxy.checked;});
  document.querySelectorAll('input[name=prev]').forEach(r=>r.addEventListener('change',()=>{$('prevYears').hidden=r.value!=='yes'||!r.checked;}));
  ['phone','pxTel'].forEach(id=>{const el=$(id);el.addEventListener('input',()=>{const v=el.value.replace(/\D/g,'').slice(0,11);el.value=v.length>7?v.replace(/(\d{3})(\d{3,4})(\d{4})/,'$1-$2-$3'):v.length>3?v.replace(/(\d{3})(\d+)/,'$1-$2'):v;});});
  ['arc','arcOld'].forEach(id=>{const el=$(id);el.addEventListener('input',()=>{const v=el.value.replace(/\D/g,'').slice(0,13);el.value=v.length>6?v.slice(0,6)+'-'+v.slice(6):v;});});
  const hd=$('hireDate');hd.addEventListener('input',()=>{const v=hd.value.replace(/\D/g,'').slice(0,8);hd.value=v.length>6?v.slice(0,4)+'-'+v.slice(4,6)+'-'+v.slice(6):v.length>4?v.slice(0,4)+'-'+v.slice(4):v;});
  const pw=$('htPw'),eye=$('pwEye');eye.onclick=()=>{const s=pw.type==='password';pw.type=s?'text':'password';eye.textContent=L()==='ko'?(s?'숨김':'보기'):(s?'Нуух':'Харах');};
  // ---- submit ----
  const toB64=f=>new Promise((res,rej)=>{const r=new FileReader();r.onload=()=>res(r.result.split(',')[1]);r.onerror=rej;r.readAsDataURL(f);});
  // 주의: XHR upload.onprogress 는 CORS 사전요청(OPTIONS)을 유발해 Apps Script에서 실패함 → fetch 유지, 진행률은 크기 기반 추정
  const postEst=(obj,bytes,onProg)=>{const est=1500+bytes/150000;const t0=Date.now();const iv=setInterval(()=>{const r=1-Math.exp(-(Date.now()-t0)/est);onProg(Math.min(0.95,r));},150);return post(obj).finally(()=>clearInterval(iv));};
  async function shrink(f){if(!f.type.startsWith('image/')||f.size<700*1024)return f;
    try{const bmp=await createImageBitmap(f);const Lm=2000,s=Math.min(1,Lm/Math.max(bmp.width,bmp.height));const c=document.createElement('canvas');c.width=Math.round(bmp.width*s);c.height=Math.round(bmp.height*s);c.getContext('2d').drawImage(bmp,0,0,c.width,c.height);
      const blob=await new Promise(r=>c.toBlob(r,'image/jpeg',0.85));if(!blob||blob.size>=f.size)return f;return new File([blob],f.name.replace(/\.[^.]+$/,'')+'.jpg',{type:'image/jpeg'});}catch(e){return f;}}
  async function post(obj){const r=await fetch(ENDPOINT,{method:'POST',headers:{'Content-Type':'text/plain;charset=utf-8'},body:JSON.stringify(obj)});if(!r.ok)throw new Error('HTTP '+r.status);return r.json();}
  let busy=false;
  $('apply').addEventListener('submit',async e=>{
    e.preventDefault();if(busy)return;const ko=L()==='ko';
    if(!ENDPOINT){showErr(3,[ko?'온라인 접수는 준비 중입니다.':'Онлайн бүртгэл бэлтгэгдэж байна.',null]);return;}
    if(!showErr(1,v1())){show(1);return;} if(!showErr(2,v2())){show(2);return;} if(!showErr(3,v3()))return;
    const all=Object.entries(store).flatMap(([role,l])=>l.map(f=>({role,f})));
    const base={lang:L(),name:g('name').toUpperCase(),arc:g('arc'),arcOld:g('arcOld'),phone:g('phone'),visa:g('visa'),addr:g('addr'),hireDate:g('hireDate'),companies:g('companies'),
      prev:document.querySelector('input[name=prev]:checked').value,prevYears:g('prevYears'),bank:g('bank'),acct:g('acct'),htId:g('htId'),htPw:g('htPw'),memo:g('memo'),
      proxy:proxy.checked?(g('pxName')+' '+g('pxTel')).trim():''};
    const btn=$('submitBtn'),prog=$('prog'),bar=$('bar'),progT=$('progT'),progP=$('progP');const setP=p=>{p=Math.max(0,Math.min(100,Math.round(p)));bar.style.width=p+'%';progP.textContent=p+'%';};
    busy=true;btn.disabled=true;prog.hidden=false;$('err3').textContent='';
    const fail=()=>{busy=false;btn.disabled=false;prog.hidden=true;$('err3').textContent=ko?'전송에 실패했습니다. 입력한 내용은 유지됩니다. 잠시 후 다시 시도하거나 담당자에게 연락해 주세요.':'Илгээж чадсангүй. Оруулсан мэдээлэл хадгалагдсан. Дахин оролдох эсвэл хариуцагчтай холбогдоно уу.';};
    let res;
    try{
      progT.textContent=ko?'접수 생성 중…':'Бүртгэл үүсгэж байна…';setP(3);
      const c=await post(Object.assign({action:'create',fileList:all.map(x=>({role:x.role,name:x.f.name,type:x.f.type,size:x.f.size}))},base));
      if(!c||!c.ok||!c.no)return fail();
      const counters={};
      for(let i=0;i<all.length;i++){const x=all[i];counters[x.role]=(counters[x.role]||0)+1;
        const p0=5+85*i/all.length,p1=5+85*(i+1)/all.length;
        progT.textContent=(ko?'파일 올리는 중 ':'Файл илгээж байна ')+(i+1)+'/'+all.length+' · '+x.f.name;setP(p0);
        const f=await shrink(x.f);const data=await toB64(f);let r=null;
        for(let t=0;t<2&&!(r&&r.ok);t++){try{r=await postEst({action:'file',no:c.no,folderId:c.folderId,idx:counters[x.role],file:{role:x.role,name:f.name,type:f.type||'application/octet-stream',data}},data.length,fr=>setP(p0+(p1-p0)*0.85*fr));}catch(ex){r=null;}}
        setP(p1);
        if(!r||!r.ok)return fail();}
      progT.textContent=ko?'마무리 중…':'Дуусгаж байна…';setP(95);
      const doneReq=Object.assign({action:'done',no:c.no,folderId:c.folderId,count:all.length,files:all.map(x=>({role:x.role,name:x.f.name}))},base);
      res=null;
      for(let t=0;t<3&&!(res&&res.ok&&res.no===c.no);t++){ // 마무리 단계 자동 재시도 (최대 3회, 3초 간격)
        if(t)await new Promise(r=>setTimeout(r,3000));
        try{res=await post(doneReq);}catch(ex){res=null;}}
      if(!res||!res.ok||res.no!==c.no)return fail();
    }catch(ex){return fail();}
    setP(100);progT.textContent=ko?'완료':'Дууслаа';
    const sum=$('summary');sum.innerHTML='';
    [[ko?'접수번호':'Бүртгэлийн №',res.no],[ko?'성명':'Нэр',base.name],[ko?'휴대폰':'Утас',base.phone],[ko?'환급계좌':'Данс',base.bank+' '+base.acct],[ko?'첨부':'Файл',all.length+(ko?'건':'')],[ko?'입력자':'Оруулсан',base.proxy||(ko?'본인':'Өөрөө')]]
      .forEach(([k,v])=>{const dt=document.createElement('dt');dt.textContent=k;const dd=document.createElement('dd');dd.textContent=v;sum.append(dt,dd);});
    $('apply').hidden=true;document.querySelector('.stepbar').hidden=true;const done=$('done');done.hidden=false;done.scrollIntoView({behavior:'smooth',block:'start'});busy=false;
  });
  function onLang(){renderAll();if(cur===3)renderReview();}
'''
    return shell('온라인 접수 — 세무법인 위드택스', body, '', js, 'apply')

for name, fn in [('index.html', INDEX), ('calc.html', CALC), ('apply.html', APPLY)]:
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(fn())
    print('wrote', name)
