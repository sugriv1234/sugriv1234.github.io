import json, os, sys
from html import escape as e
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(__file__))
from content import C, LANGS, PATHS, HREFLANG, LANG_LABEL, DOMAIN, EMAIL, LINKEDIN

OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/site2"
VER = "20261103b"
PAT = json.load(open(os.path.join(os.path.dirname(__file__), "patterns.json")))

ARROW = '<svg aria-hidden="true" viewBox="0 0 24 24" width="16" height="16"><path d="M5 12h14M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="square"/></svg>'
OUTL = '<svg aria-hidden="true" viewBox="0 0 24 24" width="15" height="15"><path d="M8 16 16 8M9 8h7v7" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="square"/></svg>'
SEARCH = '<svg aria-hidden="true" viewBox="0 0 24 24" width="19" height="19"><circle cx="11" cy="11" r="6.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="m16 16 4.5 4.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="square"/></svg>'
MAIL = '<svg aria-hidden="true" viewBox="0 0 24 24" width="17" height="17"><rect x="3.5" y="5.5" width="17" height="13" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="m4 7 8 6 8-6" fill="none" stroke="currentColor" stroke-width="1.7"/></svg>'
LI = '<svg aria-hidden="true" viewBox="0 0 24 24" width="16" height="16"><path fill="currentColor" d="M4.98 3.5A2.5 2.5 0 1 1 5 8.5a2.5 2.5 0 0 1-.02-5zM3 9.75h4V21H3zM9.5 9.75h3.8v1.6h.05c.53-1 1.83-2.05 3.77-2.05 4.03 0 4.78 2.65 4.78 6.1V21h-4v-4.95c0-1.18-.02-2.7-1.65-2.7-1.65 0-1.9 1.29-1.9 2.62V21h-4z"/></svg>'


def typo(v, fr):
    if isinstance(v, str):
        if v.startswith("/") or v.startswith("http"):
            return v
        v = v.replace("'", "’")
        if fr:
            for p in (" :", " ;", " !", " ?", "« ", " »"):
                v = v.replace(p, p.replace(" ", " "))
        return v
    if isinstance(v, list): return [typo(x, fr) for x in v]
    if isinstance(v, tuple): return tuple(typo(x, fr) for x in v)
    if isinstance(v, dict): return {k: typo(x, fr) for k, x in v.items()}
    return v


def mailto(subj):
    return f"mailto:{EMAIL}?subject={quote(subj + ' | victseng.com')}"


def pat_url(name):
    return "data:image/svg+xml," + quote(PAT[name]["svg"])


def jsonld(lang, c):
    return json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Person", "@id": DOMAIN + "/#victor", "name": "Victor Tseng",
             "alternateName": ["曾浩瑜", "Hao-yu Tseng", "Hao-yu (Victor) Tseng"],
             "jobTitle": c["job_title"], "url": DOMAIN + PATHS[lang],
             "image": DOMAIN + "/assets/img/victor-tseng.jpg", "email": "mailto:" + EMAIL,
             "address": {"@type": "PostalAddress", "addressLocality": "Abidjan", "addressCountry": "CI"},
             "worksFor": {"@id": DOMAIN + "/#consult"},
             "alumniOf": [{"@type": "CollegeOrUniversity", "name": n} for n in ("IAE Paris-Est", "HEC Paris", "National Sun Yat-sen University")],
             "knowsLanguage": ["zh", "en", "fr"],
             "knowsAbout": ["African art", "Lifestyle in Abidjan", "Cross-cultural communication", "African business", "Côte d'Ivoire", "International market development"],
             "sameAs": [LINKEDIN, DOMAIN + "/akwaba-maison/", DOMAIN + "/akwaba/"]},
            {"@type": "Organization", "@id": DOMAIN + "/#consult", "name": "VicTseng Consult", "alternateName": "維策顧問",
             "founder": {"@id": DOMAIN + "/#victor"}, "url": DOMAIN + "/"},
            {"@type": "ProfilePage", "url": DOMAIN + PATHS[lang], "inLanguage": c["html_lang"], "mainEntity": {"@id": DOMAIN + "/#victor"}},
        ]}, ensure_ascii=False)


def page(lang):
    c = typo(C[lang], lang == "fr") if lang != "zh" else C[lang]
    url = DOMAIN + PATHS[lang]
    latin = "&family=Noto+Serif:wght@500;600" if lang != "zh" else ""
    alts = "\n".join(f'<link rel="alternate" hreflang="{HREFLANG[l]}" href="{DOMAIN}{PATHS[l]}">' for l in LANGS)
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{DOMAIN}/">'
    langsw = "".join(
        f'<a href="{PATHS[l]}" hreflang="{HREFLANG[l]}" lang="{C[l]["html_lang"]}"' + (' aria-current="page"' if l == lang else "") + f">{LANG_LABEL[l]}</a>"
        for l in LANGS)
    nav = "".join(f'<a href="#{i}" data-sec="{i}"><span class="ix">{n:02d}</span>{e(t)}</a>' for n, (i, t) in enumerate(c["nav"], 1))
    domains = "".join(f'<li><a href="#x-{i+1}"><span class="ix">{i+1:02d}</span>{e(d)}</a></li>' for i, d in enumerate(c["domains"]))
    stats = "".join(f'<li><b>{e(n)}</b><span>{e(t)}</span></li>' for n, t in c["stats"])

    pillars = "".join(f"""
      <li class="pl rv" id="x-{i+1}">
        <span class="ix">{i+1:02d}</span>
        <div><h3>{e(t)}</h3><p>{e(l)}</p><ul class="tags">{''.join(f'<li>{e(s)}</li>' for s in tags)}</ul></div>
      </li>""" for i, (t, l, tags) in enumerate(c["pillars"]))

    works = "".join(f"""
      <a class="wk rv" href="{w['url']}">
        <span class="band" style="background-image:url('{pat_url(w['pat'])}');background-size:{PAT[w['pat']]['w']//2*2}px" aria-hidden="true"></span>
        <span class="wk-in">
          <span class="cap">{e(w['sub'])}</span>
          <span class="wk-t">{e(w['name'])}</span>
          <span class="wk-l">{e(w['line'])}</span>
          <span class="facts">{' <i>/</i> '.join(e(f) for f in w['facts'])}</span>
          <span class="go">{e(w['cta'])} {ARROW}</span>
        </span>
      </a>""" for w in c["works"])

    arts = "".join(f"""
      <li class="rv"><a class="ar" href="{u}" target="_blank" rel="noopener">
        <span class="ar-m"><span class="mono">{e(d)}</span><span class="cap">{e(o)}</span>{f'<span class="badge">{e(lg)}</span>' if lg else ''}</span>
        <span class="ar-t">{e(t)}</span>{OUTL}
      </a></li>""" for d, o, t, u, lg in c["articles"])

    def job(j):
        y, r, o, p, d = j
        return f'<li><span class="mono y">{e(y)}</span><div><h4>{e(r)}</h4><p class="org">{e(o)}<span> · {e(p)}</span></p><p class="d">{e(d)}</p></div></li>'
    jobs_main = "".join(job(j) for j in c["jobs"][:5])
    jobs_more = "".join(job(j) for j in c["jobs"][5:])
    edu = "".join(f'<li><span class="mono y">{e(y)}</span><div><h4>{e(d)}</h4><p class="org">{e(s)}</p></div></li>' for y, d, s in c["edu"])

    # search index (current language)
    idx = []
    for i, (t, l, tags) in enumerate(c["pillars"]):
        idx.append({"t": t, "s": c["sec_expertise"], "d": l + " " + " ".join(tags), "h": f"#x-{i+1}"})
    for w in c["works"]:
        idx.append({"t": w["name"], "s": c["sec_work"], "d": w["line"] + " " + " ".join(w["facts"]) + " AKWABA Côte d'Ivoire 象牙海岸", "h": w["url"]})
    for d, o, t, u, lg in c["articles"]:
        idx.append({"t": t, "s": c["sec_writing_t"], "d": o + " " + d, "h": u})
    for y, r, o, p, d in c["jobs"]:
        idx.append({"t": r, "s": f"{c['sec_exp']} · {o}", "d": f"{o} {p} {d} {y}", "h": "#experience"})
    for y, d, s in c["edu"]:
        idx.append({"t": d, "s": f"{c['edu_t']} · {s}", "d": s + " " + y, "h": "#experience"})
    idx.append({"t": c["contact_t"], "s": c["sec_contact"], "d": EMAIL + " LinkedIn email " + c["email_btn"], "h": "#contact"})
    idx_json = json.dumps(idx, ensure_ascii=False).replace("</", "<\\/")

    ui = json.dumps({"none": c["search_none"]}, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="{c['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(c['title'])}</title>
<meta name="description" content="{e(c['description'])}">
<meta name="author" content="Victor Tseng 曾浩瑜">
<link rel="canonical" href="{url}">
{alts}
<meta property="og:type" content="profile">
<meta property="og:site_name" content="Victor Tseng 曾浩瑜">
<meta property="og:title" content="{e(c['title'])}">
<meta property="og:description" content="{e(c['description'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}/assets/img/og-{lang}.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:locale" content="{c['og_locale']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0B0B0A">
<meta name="color-scheme" content="dark">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&family=Noto+Serif+TC:wght@500;700&family=Noto+Sans+TC:wght@400;500{latin}&display=swap">
<link rel="stylesheet" href="/assets/site.css?v={VER}">
<script>document.documentElement.classList.add('js')</script>
<script type="application/ld+json">{jsonld(lang, c)}</script>
</head>
<body class="l-{lang}">
<a class="skip" href="#main">{e(c['skip'])}</a>

<header class="hd">
  <div class="hd-row wrap">
    <a class="logo" href="{PATHS[lang]}" aria-label="Victor Tseng"><span class="logo-m">VT</span><span class="logo-t">VICTOR TSENG</span></a>
    <div class="hd-r">
      <button class="sbtn" type="button" data-open-search aria-label="{e(c['search'])}">{SEARCH}<span class="kbd">/</span></button>
      <nav class="lg" aria-label="{e(c['lang_label'])}">{langsw}</nav>
    </div>
  </div>
  <nav class="an" aria-label="{e(c['menu_label'])}"><div class="an-in wrap">{nav}</div></nav>
</header>

<main id="main">
  <section class="hero">
    <div class="wrap hero-g">
      <div class="hero-t">
        <p class="meta mono"><span class="dot" aria-hidden="true"></span>ABIDJAN <span class="co">· 05°20′N 04°01′W </span>· <span>{e(c['local_time'])}</span> <time data-clock>--:--</time> GMT</p>
        <p class="cap gold">AFRICA × ASIA <span class="sl">/</span> CROSS-CULTURAL</p>
        <h1>{c['h1']}</h1>
        <ul class="doms">{domains}</ul>
        <p class="who"><strong>{e(c['who'])}</strong><span>{e(c['role'])}</span></p>
        <p class="one">{e(c['one'])}</p>
        <div class="ctas">
          <a class="btn btn-g" href="{mailto(c['contact_subject'])}">{e(c['cta1'])} {ARROW}</a>
          <a class="btn btn-o" href="#work">{e(c['cta2'])}</a>
        </div>
      </div>
      <figure class="ph">
        <picture><source srcset="/assets/img/victor-tseng.webp" type="image/webp"><img src="/assets/img/victor-tseng.jpg" width="800" height="1000" alt="{e(c['photo_alt'])}" fetchpriority="high"></picture>
        <figcaption class="mono"><span>VT—01</span><span>ABIDJAN, CI</span></figcaption>
      </figure>
    </div>
    <div class="kita" aria-hidden="true"></div>
  </section>

  <section class="st" aria-label="Highlights"><ul class="wrap st-g">{stats}</ul></section>

  <section id="expertise" class="sec">
    <div class="wrap">
      <header class="sh rv"><span class="mono">01 / 05</span><p class="cap gold">{e(c['sec_expertise'])}</p><h2>{e(c['sec_expertise_t'])}</h2></header>
      <ol class="pls">{pillars}
      </ol>
    </div>
  </section>

  <section id="work" class="sec">
    <div class="wrap">
      <header class="sh rv"><span class="mono">02 / 05</span><p class="cap gold">{e(c['sec_work'])}</p><h2>{e(c['sec_work_t'])}</h2><p class="note">{e(c['work_note'])}</p></header>
      <div class="wks">{works}
      </div>
    </div>
  </section>

  <section id="writing" class="sec">
    <div class="wrap">
      <header class="sh rv"><span class="mono">03 / 05</span><p class="cap gold">{e(c['sec_writing'])}</p><h2>{e(c['sec_writing_t'])}</h2><p class="note">{e(c['writing_note'])}</p></header>
      <ul class="ars">{arts}
      </ul>
    </div>
  </section>

  <section id="experience" class="sec">
    <div class="wrap ex-g">
      <div>
        <header class="sh rv"><span class="mono">04 / 05</span><p class="cap gold">{e(c['sec_exp'])}</p><h2>{e(c['sec_exp_t'])}</h2></header>
        <ol class="jobs rv">{jobs_main}</ol>
        <details class="more"><summary><span>{e(c['more_jobs'])}</span><span class="mono">+{len(c['jobs'])-5}</span></summary><ol class="jobs">{jobs_more}</ol></details>
      </div>
      <aside class="ex-s rv">
        <p class="cap gold">{e(c['edu_t'])}</p>
        <ol class="jobs sm">{edu}</ol>
        <p class="cap gold">{e(c['lang_t'])}</p>
        <p class="lgs">{e(c['langs'])}</p>
        <a class="lnk" href="{mailto(c['cv_subject'])}">{e(c['cv'])} {ARROW}</a>
      </aside>
    </div>
  </section>

  <section id="contact" class="sec ct">
    <div class="wrap">
      <header class="sh rv"><span class="mono">05 / 05</span><p class="cap gold">{e(c['sec_contact'])}</p><h2>{e(c['contact_t'])}</h2><p class="note">{e(c['contact_line'])}</p></header>
      <div class="ctas rv">
        <a class="btn btn-g" href="{mailto(c['contact_subject'])}">{MAIL} {e(c['email_btn'])}</a>
        <a class="btn btn-o" href="{LINKEDIN}" target="_blank" rel="noopener me">{LI} {e(c['li_btn'])}</a>
      </div>
      <p class="mono mail">{EMAIL}</p>
    </div>
  </section>
</main>

<footer class="ft">
  <div class="kita" aria-hidden="true"></div>
  <div class="wrap ft-g">
    <p class="logo-t">VICTOR TSENG <span>曾浩瑜</span></p>
    <p class="mono">{e(c['based'])}</p>
    <p class="mono">© 2026 Victor Tseng 曾浩瑜 · VicTseng Consult</p>
    <nav class="lg" aria-label="{e(c['lang_label'])}">{langsw}</nav>
  </div>
</footer>

<div class="sr" role="dialog" aria-modal="true" aria-label="{e(c['search'])}" hidden>
  <div class="sr-box">
    <div class="sr-in">{SEARCH}<input type="search" placeholder="{e(c['search_ph'])}" autocomplete="off" aria-label="{e(c['search'])}"><button type="button" data-close-search class="mono">{e(c['search_close'])}</button></div>
    <ul class="sr-res" role="listbox"></ul>
  </div>
</div>
<script id="sidx" type="application/json">{idx_json}</script>
<script>window.UI={ui}</script>
<script src="/assets/site.js?v={VER}" defer></script>
</body>
</html>
"""


def write(path, text):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(text)


for l in LANGS:
    write((PATHS[l].strip("/") + "/index.html").lstrip("/"), page(l))

kita = pat_url("kita")
css_tpl = open(os.path.join(os.path.dirname(__file__), "site.css")).read().replace("__KITA__", kita)
write("assets/site.css", css_tpl)
write("assets/site.js", open(os.path.join(os.path.dirname(__file__), "site.js")).read())

urls = "\n".join("  <url><loc>{0}{1}</loc>{2}</url>".format(DOMAIN, PATHS[l], "".join(
    f'<xhtml:link rel="alternate" hreflang="{HREFLANG[x]}" href="{DOMAIN}{PATHS[x]}"/>' for x in LANGS)) for l in LANGS)
write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n{urls}\n</urlset>\n')
write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
write("CNAME", "victseng.com\n")
write("404.html", f"""<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>404 · Victor Tseng</title><meta name="robots" content="noindex"><link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jost:wght@300;500&family=IBM+Plex+Mono&display=swap"><link rel="stylesheet" href="/assets/site.css?v={VER}"></head>
<body><main class="nf"><p class="mono gold">ERROR 404</p><p class="nf-n">404</p><p>找不到這個頁面 · Page not found · Page introuvable</p><p class="ctas"><a class="btn btn-g" href="/">中文</a><a class="btn btn-o" href="/en/">English</a><a class="btn btn-o" href="/fr/">Français</a></p></main></body></html>
""")
print("built", OUT)
