const { chromium } = require('playwright'); const fs=require('fs');
const photo='data:image/jpeg;base64,'+fs.readFileSync('/home/claude/site2/assets/img/victor-tseng.jpg').toString('base64');
const P=JSON.parse(fs.readFileSync('patterns.json')); const kita='data:image/svg+xml,'+encodeURIComponent(P.kita.svg);
const L={zh:{h:'讀懂非洲的<br>藝術、生活與生意',n:'曾浩瑜 Victor Tseng',r:'跨文化市場開發顧問',f:"'Noto Serif CJK TC',serif",w:700},
 en:{h:'Reading Africa:<br>art, lifestyle and business',n:'Victor Tseng 曾浩瑜',r:'CROSS-CULTURAL MARKET DEVELOPMENT',f:"'DejaVu Serif',Georgia,serif",w:400},
 fr:{h:'Lire l’Afrique :<br>son art, sa vie, ses affaires',n:'Victor Tseng 曾浩瑜',r:'DÉVELOPPEMENT DE MARCHÉS · INTERCULTUREL',f:"'DejaVu Serif',Georgia,serif",w:400}};
(async()=>{const b=await chromium.launch();
for(const [k,v] of Object.entries(L)){const p=await b.newPage({viewport:{width:1200,height:630}});
await p.setContent(`<html><body style="margin:0;width:1200px;height:630px;background:#0B0B0A;color:#F2EDE4;font-family:Inter,'Noto Sans CJK TC',sans-serif;position:relative;overflow:hidden">
<div style="position:absolute;inset:0;background-image:linear-gradient(rgba(242,237,228,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(242,237,228,.06) 1px,transparent 1px);background-size:56px 56px"></div>
<div style="position:absolute;left:0;right:0;bottom:0;height:16px;background:url('${kita}');background-size:32px 32px"></div>
<div style="position:absolute;left:72px;top:70px;width:640px">
 <div style="display:flex;align-items:center;gap:14px"><div style="width:40px;height:40px;border:1.5px solid #C9A34E;display:grid;place-items:center;color:#C9A34E;font:500 14px Inter;letter-spacing:2px">VT</div><div style="font:500 16px Inter;letter-spacing:7px">VICTOR TSENG</div></div>
 <div style="margin-top:58px;font:600 13px Inter;letter-spacing:6px;color:#C9A34E">AFRICA × ASIA &nbsp;/&nbsp; CROSS-CULTURAL</div>
 <div style="margin-top:20px;font:${v.w} 52px/1.22 ${v.f};letter-spacing:.5px">${v.h}</div>
 <div style="margin-top:40px;padding-top:20px;border-top:1px solid rgba(242,237,228,.18);display:flex;gap:16px;align-items:baseline"><span style="font:600 20px 'Noto Serif CJK TC',serif">${v.n}</span><span style="font:500 13px Inter,'Noto Sans CJK TC';letter-spacing:3px;color:#C9A34E">${v.r}</span></div>
 <div style="margin-top:14px;font:400 14px 'DejaVu Sans Mono';color:#9C9385;letter-spacing:1px">victseng.com · ABIDJAN, CÔTE D’IVOIRE</div>
</div>
<div style="position:absolute;right:72px;top:62px;width:330px;height:440px">
 <div style="position:absolute;inset:12px -12px -12px 12px;border:1px solid rgba(201,163,78,.6)"></div>
 <img src="${photo}" style="position:relative;width:330px;height:440px;object-fit:cover;object-position:50% 20%;filter:saturate(.88) contrast(1.04)">
</div></body></html>`);
await p.screenshot({path:`/home/claude/site2/assets/img/og-${k}.jpg`,type:'jpeg',quality:86});await p.close();}
const p=await b.newPage({viewport:{width:180,height:180}});
await p.setContent(`<html><body style="margin:0;width:180px;height:180px;background:#0B0B0A;display:grid;place-items:center"><div style="width:140px;height:140px;border:4px solid #C9A34E;display:grid;place-items:center;color:#C9A34E;font:500 52px Inter;letter-spacing:6px;padding-left:6px">VT</div></body></html>`);
await p.screenshot({path:'/home/claude/site2/assets/img/apple-touch-icon.png'});await b.close();})();
