// Renders social preview images + icons. Run: node og.js <site_dir>
const { chromium } = require('playwright'); const fs=require('fs'); const out=process.argv[2]||'..';
const photo='data:image/jpeg;base64,'+fs.readFileSync(out+'/assets/img/victor-tseng.jpg').toString('base64');
const P=JSON.parse(fs.readFileSync(__dirname+'/patterns.json')); const kita='data:image/svg+xml,'+encodeURIComponent(P.kita_light.svg);
const L={zh:{h:'讀懂非洲的<br>藝術、生活與生意',n:'曾浩瑜 Victor Tseng',r:'跨文化市場開發顧問',f:"'Noto Serif TC','Noto Serif CJK TC',serif",s:58},
 en:{h:'Reading Africa:<br>art, lifestyle and business',n:'Victor Tseng 曾浩瑜',r:'CROSS-CULTURAL MARKET DEVELOPMENT',f:"'Cormorant Garamond','DejaVu Serif',serif",s:62},
 fr:{h:'Lire l’Afrique :<br>son art, sa vie, ses affaires',n:'Victor Tseng 曾浩瑜',r:'DÉVELOPPEMENT DE MARCHÉS · INTERCULTUREL',f:"'Cormorant Garamond','DejaVu Serif',serif",s:62}};
(async()=>{const b=await chromium.launch();
for(const [k,v] of Object.entries(L)){const p=await b.newPage({viewport:{width:1200,height:630}});
await p.setContent(`<html><body style="margin:0;width:1200px;height:630px;background:#F4EFE7;color:#161412;font-family:Jost,Inter,'Noto Sans CJK TC',sans-serif;position:relative;overflow:hidden">
<div style="position:absolute;left:0;right:0;bottom:0;height:14px;background:url('${kita}');background-size:24px 24px"></div>
<div style="position:absolute;left:80px;top:74px;font:400 15px Jost,Inter;letter-spacing:8px">VICTOR TSENG</div>
<div style="position:absolute;left:80px;top:170px;width:680px">
 <div style="font:400 12px Jost,Inter;letter-spacing:6px;color:#A8874A">AFRICA × ASIA — CROSS-CULTURAL</div>
 <div style="margin-top:24px;font:400 ${v.s}px/1.18 ${v.f};letter-spacing:${k==='zh'?'4px':'0'}">${v.h}</div>
 <div style="margin-top:40px;width:60px;height:1px;background:#A8874A"></div>
 <div style="margin-top:22px;font:500 20px 'Noto Serif CJK TC',serif;letter-spacing:2px">${v.n}</div>
 <div style="margin-top:10px;font:400 12px Jost,Inter,'Noto Sans CJK TC';letter-spacing:5px;color:#7C7266">${v.r} · VICTSENG.COM</div>
</div>
<div style="position:absolute;right:96px;top:92px;width:290px;height:390px">
 <div style="position:absolute;inset:-10px;border:1px solid #A8874A;border-radius:999px 999px 0 0;opacity:.8"></div>
 <img src="${photo}" style="width:290px;height:390px;object-fit:cover;object-position:50% 18%;border-radius:999px 999px 0 0;filter:saturate(.82) contrast(1.03)">
</div></body></html>`);
await p.screenshot({path:`${out}/assets/img/og-${k}.jpg`,type:'jpeg',quality:86});await p.close();}
const p=await b.newPage({viewport:{width:180,height:180}});
await p.setContent(`<html><body style="margin:0;width:180px;height:180px;background:#161412;display:grid;place-items:center"><div style="font:400 64px 'DejaVu Serif',serif;color:#F4EFE7;letter-spacing:4px">VT</div></body></html>`);
await p.screenshot({path:`${out}/assets/img/apple-touch-icon.png`});await b.close();})();
