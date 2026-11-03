# victseng.com

Victor Tseng 曾浩瑜 的個人網站（作者中心），三語：繁中 `/`、English `/en/`、Français `/fr/`。

- 規則：網站上不寫目前的雇主；媒體文章只放索引（標題、日期、媒體、一句新寫的介紹、連結），不轉載、不翻譯投稿內文。

© 2026 Victor Tseng 曾浩瑜

## 怎麼更新

網站由 `_src/` 裡的檔案產生（GitHub Pages 不會公開以底線開頭的資料夾）：

- 改文字：`_src/content.py`（三語都在這裡）
- 改樣式：`_src/site.css`、互動：`_src/site.js`
- 產生網站：`cd _src && python3 build.py ..`
- 新增一篇媒體文章：在三語的 `articles` 各加一筆（日期、媒體、標題、連結），只放索引，不放內文
