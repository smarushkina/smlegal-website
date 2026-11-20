# -*- coding: utf-8 -*-
"""Static site generator for SM Legal (smlegal.bg). Run: python3 build.py"""
import os, json, shutil, html, datetime, posixpath
from content_practice1 import PRACTICES_1
from content_practice2 import PRACTICES_2
from content_insights import INSIGHTS

SITE = "https://smlegal.bg"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")
PRACTICES = PRACTICES_1 + PRACTICES_2
NEW_KEYS = {"startups", "tax", "compliance"}
EMAIL = "smarushkina@smlegal.bg"
# Google Analytics 4 measurement ID (e.g. "G-XXXXXXX"). Leave empty to run without analytics.
# Analytics loads ONLY after the visitor accepts analytics cookies in the cookie banner.
GA_ID = ""
TODAY = datetime.date(2026, 10, 6).isoformat()
P = {p["key"]: p for p in PRACTICES}
import hashlib
def _ver(*files):
    """Short content hash for cache-busting (?v=…) so browsers always load the current CSS/JS."""
    h = hashlib.sha1()
    for f in files:
        with open(os.path.join(ROOT, f), "rb") as fh: h.update(fh.read())
    return h.hexdigest()[:10]
CSS_VER = _ver("assets/css/style.css", "assets/css/fonts.css")
JS_VER = _ver("assets/js/main.js")
esc = html.escape

# ---------------------------------------------------------------- routes
ROUTES = {
 "home":     {"bg": "index.html",          "en": "en/index.html"},
 "about":    {"bg": "za-nas.html",         "en": "en/about.html"},
 "practice": {"bg": "pravni-uslugi.html",  "en": "en/practice-areas.html"},
 "team":     {"bg": "ekip.html",           "en": "en/team.html"},
 "insights": {"bg": "publikatsii.html",    "en": "en/insights.html"},
 "contact":  {"bg": "kontakti.html",       "en": "en/contact.html"},
 "privacy":  {"bg": "poveritelnost.html",  "en": "en/privacy.html"},
}
def practice_path(key, lang):
    return ("pravni-uslugi/" if lang == "bg" else "en/practice-areas/") + P[key][lang]["slug"] + ".html"
def post_path(post, lang):
    return ("publikatsii/" if lang == "bg" else "en/insights/") + post[lang]["slug"] + ".html"
def url(path):
    if path.endswith("index.html"):
        path = path[: -len("index.html")]
    return SITE + "/" + path
def rel(frm, to):
    r = posixpath.relpath(to, posixpath.dirname(frm) or ".")
    return r

# ---------------------------------------------------------------- strings
T = {
 "bg": {
  "brand_sub": "Адвокатско дружество Марушкина",
  "nav": [("home","Начало"),("about","За нас"),("practice","Правни услуги"),("insights","Публикации"),("contact","Контакти")],
  "cta": "Заявете консултация", "more": "Научете повече", "read": "Прочетете", "all_practices": "Всички правни услуги",
  "all_posts": "Всички публикации", "news": "Новина", "article": "Статия", "min": "мин. четене",
  "services": "Обхват на правната помощ", "approach": "Нашият подход", "faq": "Често задавани въпроси", "other_areas": "Други практики",
  "related": "Свързани публикации", "new": "Ново", "address": "ул. „Добротица Деспот“ 41, София 1612",
  "address_l": "Адрес", "email_l": "Имейл", "hours_l": "Работно време", "hours": "Понеделник – петък, 9:30 – 18:00 ч.",
  "langs_l": "Езици на обслужване", "langs": "български, английски",
  "foot_about": "Ние посвещаваме времето, работата и усилията си, за да продължава вашият бизнес да расте.",
  "foot_practices": "Правни услуги", "foot_firm": "Кантората", "foot_visit": "Посетете ни",
  "rights": "Всички права запазени.", "privacy": "Политика за поверителност",
  "disclaimer": "Настоящата публикация има информационен характер и не представлява правна консултация. За становище по конкретен случай, моля, свържете се с нас.",
  "home_l": "Начало", "skip": "Към съдържанието", "menu": "Меню", "back_top": "Към началото",
  "cta_band_h": "Имате нужда от правна консултация?",
  "cta_band_p": "Опишете накратко въпроса си — ще се свържем с вас в рамките на един работен ден.",
  "filter_all": "Всички", "filter_news": "Новини", "filter_articles": "Статии",
  "author": "Силвия Марушкина", "author_role": "Адвокат, основател на SM Legal",
  "ck_h": "Бисквитки", "ck_p": "Използваме само необходимите за работата на сайта технически средства. С ваше съгласие бихме използвали и аналитични бисквитки, за да подобряваме сайта.",
  "ck_more": "Научете повече", "ck_accept": "Приемам всички", "ck_reject": "Само необходимите", "ck_settings": "Настройки",
  "ck_save": "Запази избора", "ck_nec": "Необходими", "ck_nec_d": "Запомнят избора ви за бисквитките. Винаги активни.",
  "ck_an": "Аналитични", "ck_an_d": "Анонимна статистика за посещенията (Google Analytics). Само с ваше съгласие.", "ck_link": "Настройки за бисквитки",
  "qo": "„", "qc": "“", "locale": "bg_BG", "months": ["януари","февруари","март","април","май","юни","юли","август","септември","октомври","ноември","декември"],
 },
 "en": {
  "brand_sub": "Marushkina Law Firm",
  "nav": [("home","Home"),("about","About"),("practice","Practice Areas"),("insights","Insights"),("contact","Contact")],
  "cta": "Request a consultation", "more": "Learn more", "read": "Read", "all_practices": "All practice areas",
  "all_posts": "All insights", "news": "News", "article": "Article", "min": "min read",
  "services": "Our services", "approach": "Our approach", "faq": "Frequently asked questions", "other_areas": "Other practice areas",
  "related": "Related insights", "new": "New", "address": "41 Dobrotitsa Despot Str., Sofia 1612, Bulgaria",
  "address_l": "Address", "email_l": "Email", "hours_l": "Office hours", "hours": "Monday – Friday, 9:30 am – 6:00 pm",
  "langs_l": "Languages", "langs": "Bulgarian, English",
  "foot_about": "We dedicate our time, work and efforts to keep your business growing.",
  "foot_practices": "Practice areas", "foot_firm": "The firm", "foot_visit": "Visit us",
  "rights": "All rights reserved.", "privacy": "Privacy policy",
  "disclaimer": "This publication is for information purposes only and does not constitute legal advice. For advice on a specific matter, please contact us.",
  "home_l": "Home", "skip": "Skip to content", "menu": "Menu", "back_top": "Back to top",
  "cta_band_h": "Need legal advice?",
  "cta_band_p": "Get in touch — we will respond within one business day.",
  "filter_all": "All", "filter_news": "News", "filter_articles": "Articles",
  "author": "Sylvia Marushkina", "author_role": "Attorney-at-law, Founder of SM Legal",
  "ck_h": "Cookies", "ck_p": "We only use the technical means needed for this website to work. With your consent, we would also use analytics cookies to improve the site.",
  "ck_more": "Learn more", "ck_accept": "Accept all", "ck_reject": "Necessary only", "ck_settings": "Settings",
  "ck_save": "Save choice", "ck_nec": "Necessary", "ck_nec_d": "Remember your cookie choice. Always active.",
  "ck_an": "Analytics", "ck_an_d": "Anonymous visit statistics (Google Analytics). Only with your consent.", "ck_link": "Cookie settings",
  "qo": "“", "qc": "”", "locale": "en_GB", "months": ["January","February","March","April","May","June","July","August","September","October","November","December"],
 },
}
def fmt_date(d, lang):
    y, m, dd = map(int, d.split("-"))
    mo = T[lang]["months"][m - 1]
    return f"{dd} {mo} {y}" + (" г." if lang == "bg" else "")

TESTIMONIALS = [
 {"name": "Ivan Pepelov", "name_bg": "Иван Пепелов", "role_en": "CEO, IDVKM", "role_bg": "Изпълнителен директор, IDVKM",
  "en": "Sylvia Marushkina is extremely competent and reliable. Since the foundation of our company, she has advised us on legal matters, even when the case was not simple, and the time frame was very short. Her flexibility, analytical thinking and problem-solving skills are one of a kind!",
  "bg": "Силвия Марушкина е изключително компетентна и надеждна. От създаването на компанията ни тя ни консултира по правни въпроси, дори когато случаят не беше лесен, а сроковете бяха изключително кратки. Нейната гъвкавост, аналитично мислене и умение да решава проблеми са несравними!"},
 {"name": "Angel Angelov", "name_bg": "Ангел Ангелов", "role_en": "Manager, Dynax Invest", "role_bg": "Управител, Dynax Invest",
  "en": "Extremely happy with the professional services of the company. Very quick reaction and in-depth coverage of different matters in the commercial law space. Reasonable pricing and enough attention to detail.",
  "bg": "Изключително доволен съм от професионалните услуги на кантората. Много бърза реакция и задълбочено покритие на различни въпроси в областта на търговското право. Разумни цени и внимание към детайла."},
 {"name": "Diana Dobreva", "name_bg": "Диана Добрева", "role_en": "Manager, My CFO", "role_bg": "Управител, My CFO",
  "en": "Every time I work with SM Legal I receive deep knowledge of corporate law and high-quality legal services. Sylvia has shown serious commitment to the work process, high professionalism and eagerness to resolve every case.",
  "bg": "Всеки път, когато работя със SM Legal, получавам задълбочено познаване на корпоративното право и висококачествени правни услуги. Силвия демонстрира сериозна отдаденост, висок професионализъм и желание да разреши всеки казус."},
 {"name": "Ioannis Kesisis", "name_bg": "Йоанис Кесисис", "role_en": "Client", "role_bg": "Клиент",
  "en": "We have had the pleasure of using the legal services of Attorney Marushkina for approximately two years now. She is analytical, with in-depth knowledge of commercial, civil and labour law. Responsive and very disciplined, she always puts herself in the client's position and offers the most adequate and favourable solution. A partner you can count on, rely on and trust.",
  "bg": "От около две години имаме удоволствието да ползваме правните услуги на адв. Марушкина. Тя е аналитичен човек със задълбочени познания в търговското, гражданското и трудовото право. Отзивчива и много дисциплинирана, тя винаги се поставя на мястото на клиента и предлага най-адекватното и благоприятно решение. Партньор, на когото можете да разчитате и да се доверите."},
]
PARTNERS = [("ImPack","ImPack_logo-01-2.jpg"),("Innovation Capital","InnovationCapital_logo.png"),("My CFO","MyCFO.jpg"),
            ("RILABS","RILABS.jpg"),("XLRADAR","XLRADAR.png"),("IDVKM","IDVKM.jpg"),("Dynax Invest","Dynax-003.jpg")]

# ---------------------------------------------------------------- icons
ICONS = {
 "building": '<path d="M4 21h16M6 21V5l6-2 6 2v16M10 8h.01M14 8h.01M10 12h.01M14 12h.01M10 16h4v5h-4z"/>',
 "chart": '<path d="M3 21h18M5 17l4-5 4 3 6-8"/><path d="M15 7h4v4"/>',
 "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M18 6l-2.5 2.5M8.5 15.5 6 18"/><circle cx="12" cy="12" r="2.2"/>',
 "people": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><circle cx="17" cy="9" r="2.4"/><path d="M16 14.2c2.9.4 5 2.8 5 5.8"/>',
 "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.8 3.8 5.8 3.8 9s-1.2 6.2-3.8 9c-2.6-2.8-3.8-5.8-3.8-9S9.4 5.8 12 3z"/>',
 "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 6a3 3 0 0 0 6 0L5 7zM19 7l-3 6a3 3 0 0 0 6 0l-3-6z"/>',
 "shield": '<path d="M12 3 5 6v5c0 4.5 3 8.3 7 10 4-1.7 7-5.5 7-10V6l-7-3z"/><path d="m9 12 2 2 4-4"/>',
 "lock": '<rect x="5" y="10.5" width="14" height="10" rx="1"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3M12 14.5v2.5"/>',
 "mark": '<circle cx="12" cy="12" r="9"/><path d="M9.5 16.5v-9h3.2a2.6 2.6 0 0 1 0 5.2H9.5M12.5 12.7l2.4 3.8"/>',
 "key": '<path d="M3 21V10l9-7 9 7v11H3z"/><path d="M9 21v-6h6v6"/>',
 "gavel": '<path d="m14 4 6 6M11 7l6 6M12.5 5.5l-4 4 6 6 4-4M9.5 12.5 3 19l2 2 6.5-6.5M13 21h8"/>',
 "pin": '<path d="M12 21s-7-6.1-7-11.5A7 7 0 0 1 19 9.5C19 14.9 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
 "mail": '<rect x="3" y="5" width="18" height="14" rx="1"/><path d="m3 6 9 7 9-7"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "chat": '<path d="M4 5h16v11H8l-4 4V5z"/><path d="M8 9.5h8M8 12.5h5"/>',
 "up": '<path d="M12 19V5M5 12l7-7 7 7"/>',
 "menu": '<path d="M3 7h18M3 12h18M3 17h18"/>',
}
def icon(name, cls=""):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'

def logo(href, light=True, tag="a", variant=None):
    """Brand logo (vector, traced from the firm's own logo files)."""
    v = variant or "logo-dark"
    src = posixpath.join(posixpath.dirname(href) if "/" in href else "", "assets/img/brand/" + v + ".svg")
    return (f'<a class="logo" href="{href}"><img src="{{LOGO_PREFIX}}assets/img/brand/{v}.svg" alt="SM Legal — Marushkina Law Firm" width="551" height="220"></a>')

# ---------------------------------------------------------------- layout
ORG_ID = SITE + "/#organization"
PERSON_ID = SITE + "/#sylvia-marushkina"
def org_schema():
    return {
     "@type": ["LegalService", "Organization"], "@id": ORG_ID,
     "name": "SM Legal — Marushkina Law Firm", "alternateName": ["SM Legal", "Адвокатско дружество Марушкина"],
     "url": SITE + "/", "logo": SITE + "/assets/img/brand/logo-dark.svg", "image": SITE + "/assets/img/og-image.png",
     "email": EMAIL, "priceRange": "€€",
     "address": {"@type": "PostalAddress", "streetAddress": "ул. Добротица Деспот 41", "addressLocality": "София",
                 "postalCode": "1612", "addressCountry": "BG"},
     "areaServed": ["BG", "EU"], "knowsLanguage": ["bg", "en"],
     "founder": {"@id": PERSON_ID},
     "knowsAbout": [P[k]["en"]["title"] for k in P],
    }

def head(lang, path, title, desc, alt_path=None, og_type="website", schema=None, noindex=False):
    t = T[lang]
    alt_lang = "en" if lang == "bg" else "bg"
    links = [f'<link rel="canonical" href="{url(path)}">']
    if alt_path:
        bgp = path if lang == "bg" else alt_path
        enp = path if lang == "en" else alt_path
        links += [f'<link rel="alternate" hreflang="bg" href="{url(bgp)}">',
                  f'<link rel="alternate" hreflang="en" href="{url(enp)}">',
                  f'<link rel="alternate" hreflang="x-default" href="{url(bgp)}">']
    css = rel(path, "assets/css/style.css") + "?v=" + CSS_VER
    fav = rel(path, "assets/img/favicon.svg")
    ogimg = SITE + "/assets/img/og-image.png"
    graph = [org_schema()] + (schema or [])
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    robots = '<meta name="robots" content="noindex, follow">' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">'
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>document.documentElement.classList.add("js")</script>
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}
{chr(10).join(links)}
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="SM Legal">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url(path)}">
<meta property="og:image" content="{ogimg}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:locale" content="{t['locale']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#4e525a">
<link rel="icon" href="{fav}" type="image/svg+xml">
<link rel="apple-touch-icon" href="{rel(path, 'assets/img/apple-touch-icon.png')}">
<link rel="preload" href="{rel(path, 'assets/fonts/raleway-cyrillic-400-normal.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{rel(path, 'assets/css/fonts.css')}?v={CSS_VER}">
<link rel="stylesheet" href="{css}">
<script type="application/ld+json">
{ld}
</script>
</head>
"""

def header(lang, path, active, alt_path):
    t = T[lang]
    items = []
    for key, label in t["nav"]:
        if key == "contact":
            continue
        cur = ' aria-current="page"' if key == active else ""
        items.append(f'<a href="{rel(path, ROUTES[key][lang])}"{cur}>{label}</a>')
    items.append(f'<a class="btn" href="{rel(path, ROUTES["contact"][lang])}"{" aria-current=page" if active=="contact" else ""}>{t["nav"][-1][1]}</a>')
    if alt_path:
        if lang == "bg":
            sw = f'<div class="lang"><span>BG</span><a href="{rel(path, alt_path)}" hreflang="en" lang="en">EN</a></div>'
        else:
            sw = f'<div class="lang"><a href="{rel(path, alt_path)}" hreflang="bg" lang="bg">BG</a><span>EN</span></div>'
    else:
        sw = ""
    return f"""<body>
<a class="skip" href="#main">{t['skip']}</a>
<header class="site-header">
 <div class="wrap">
  {logo(rel(path, ROUTES['home'][lang]), variant='logo-rose').replace('{LOGO_PREFIX}', rel(path, 'x')[:-1])}
  <button class="burger" aria-controls="nav" aria-expanded="false" aria-label="{t['menu']}">{icon('menu')}</button>
  <nav class="nav" id="nav" aria-label="{t['menu']}">
   {''.join(items)}
   {sw}
  </nav>
 </div>
</header>
<main id="main">
"""

def footer(lang, path):
    t = T[lang]
    firm = "".join(f'<li><a href="{rel(path, ROUTES[k][lang])}">{l}</a></li>' for k, l in t["nav"] if k != "home")
    return f"""</main>
<footer class="site-footer">
 <div class="wrap">
  <div class="foot-grid">
   <div>
    {logo(rel(path, ROUTES['home'][lang]), variant='logo-rose').replace('{LOGO_PREFIX}', rel(path, 'x')[:-1])}
    <p>{t['foot_about']}</p>
   </div>
   <div class="foot-contact-col"><h4>{t['foot_visit']}</h4>
    <p class="foot-addr">{icon('pin')}<span>{t['address']}</span></p>
    <p class="foot-addr">{icon('mail')}<a href="mailto:{EMAIL}">{EMAIL}</a></p>
   </div>
   <div><h4>{t['foot_firm']}</h4><ul>{firm}</ul></div>
  </div>
  <div class="foot-bottom"><span>© 2026 SM Legal — {t['brand_sub']}. {t['rights']}</span><span class="foot-links"><a href="{rel(path, ROUTES['privacy'][lang])}">{t['privacy']}</a><button type="button" class="linklike" data-cookie-open>{t['ck_link']}</button></span></div>
 </div>
</footer>
<a class="to-top" href="#main" aria-label="{t['back_top']}">{icon('up')}</a>
{cookie_banner(lang, path)}
<script src="{rel(path, 'assets/js/main.js')}?v={JS_VER}" defer></script>
</body>
</html>
"""

def cookie_banner(lang, path):
    t = T[lang]
    return f"""<div class="cookie" id="cookie" role="dialog" aria-modal="false" aria-labelledby="cookie-h" data-ga="{GA_ID}" hidden>
 <div class="cookie__in">
  <div class="cookie__txt"><h2 id="cookie-h">{t['ck_h']}</h2><p>{t['ck_p']} <a href="{rel(path, ROUTES['privacy'][lang])}#cookies">{t['ck_more']}</a></p></div>
  <div class="cookie__opts" id="cookie-opts" hidden>
   <label class="cookie__opt"><input type="checkbox" checked disabled><span><strong>{t['ck_nec']}</strong>{t['ck_nec_d']}</span></label>
   <label class="cookie__opt"><input type="checkbox" data-cookie-analytics><span><strong>{t['ck_an']}</strong>{t['ck_an_d']}</span></label>
  </div>
  <div class="cookie__btns">
   <button type="button" class="btn btn--ghost" data-cookie="settings" aria-controls="cookie-opts" aria-expanded="false">{t['ck_settings']}</button>
   <button type="button" class="btn btn--ghost" data-cookie="reject">{t['ck_reject']}</button>
   <button type="button" class="btn btn--ghost" data-cookie="save" hidden>{t['ck_save']}</button>
   <button type="button" class="btn" data-cookie="accept">{t['ck_accept']}</button>
  </div>
 </div>
</div>"""

def crumbs(lang, path, trail):
    """trail: list of (label, path or None)"""
    t = T[lang]
    full = [(t["home_l"], ROUTES["home"][lang])] + trail
    lis = []
    for label, p in full:
        if p and p != path:
            lis.append(f'<li><a href="{rel(path, p)}">{esc(label)}</a></li>')
        else:
            lis.append(f'<li aria-current="page">{esc(label)}</li>')
    schema = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": label, "item": url(p or path)} for i, (label, p) in enumerate(full)]}
    return f'<nav class="crumbs" aria-label="breadcrumb"><ol>{"".join(lis)}</ol></nav>', schema

def page_hero(lang, path, trail, h1, sub, eyebrow=""):
    c, s = crumbs(lang, path, trail)
    eb = f'<span class="eyebrow">{esc(eyebrow)}</span>' if eyebrow else ""
    return f'<section class="page-hero dark"><div class="wrap">{c}{eb}<h1>{esc(h1)}</h1>{"<p>"+esc(sub)+"</p>" if sub else ""}</div></section>', s

def cta_band(lang, path):
    t = T[lang]
    return f"""<section class="cta-band dark"><div class="wrap"><div><h2>{t['cta_band_h']}</h2><p>{t['cta_band_p']}</p></div>
<a class="btn btn--rose" href="{rel(path, ROUTES['contact'][lang])}">{t['cta']}</a></div></section>"""

def cta_card(lang, path):
    t = T[lang]
    h = "Не откривате нужната услуга?" if lang == "bg" else "Can't find what you need?"
    p = "Опишете ни вашия въпрос — ще ви насочим към правилното решение или доверен партньор." if lang == "bg" else "Tell us about your matter — we will point you to the right solution or a trusted partner."
    return f'''<article class="card card--cta reveal">{icon('chat', 'card__icon')}<h3><a href="{rel(path, ROUTES['contact'][lang])}">{h}</a></h3><p>{p}</p><span class="link-arrow">{t['cta']}</span></article>'''

def practice_card(p, lang, path):
    t = T[lang]
    d = p[lang]
    new = " card--new" if p["key"] in NEW_KEYS else ""
    badge = f'<span class="badge-new">{t["new"]}</span>' if new else ""
    return f"""<article class="card reveal{new}">{badge}{icon(p['icon'], 'card__icon')}
<h3><a href="{rel(path, practice_path(p['key'], lang))}">{esc(d['title'])}</a></h3><p>{esc(d['short'])}</p><span class="link-arrow">{t['more']}</span></article>"""

def post_card(post, lang, path):
    t = T[lang]
    d = post[lang]
    typ = t["news"] if post["type"] == "news" else t["article"]
    return f"""<article class="post reveal" data-type="{post['type']}" data-practice="{post['practice']}"><div class="post__top"></div><div class="post__body">
<div class="post__meta"><span class="badge">{typ}</span><time datetime="{post['date']}">{fmt_date(post['date'], lang)}</time></div>
<h3><a href="{rel(path, post_path(post, lang))}">{esc(d['title'])}</a></h3><p>{esc(d['excerpt'])}</p><span class="link-arrow">{t['read']}</span></div></article>"""

def sorted_posts():
    return sorted(INSIGHTS, key=lambda x: x["date"], reverse=True)

PAGES = []  # (path, html, lang, alt_path, lastmod)
def emit(path, html_doc, lang=None, alt=None, lastmod=TODAY, sitemap=True):
    PAGES.append({"path": path, "html": html_doc, "lang": lang, "alt": alt, "lastmod": lastmod, "sitemap": sitemap})

# ---------------------------------------------------------------- pages
HOME = {
 "bg": {
  "title": "SM Legal — Адвокатско дружество Марушкина | Бизнес адвокат в София",
  "desc": "SM Legal — адвокатска кантора в София с практика в бизнес правото: търговско и корпоративно право, рисков капитал, стартъпи, трудово и имиграционно право, данъци, корпоративно съответствие, защита на личните данни, търговски марки и спорове.",
  "eyebrow": "Адвокатска кантора · София",
  "h1": "Правна сигурност <em>на всеки етап</em> от развитието на вашия бизнес",
  "lead": '<span class="brand-inline">SM Legal</span> предоставя правна помощ с внимание към всеки детайл и към конкретните цели на клиента. Всеки възложен казус получава задълбочен анализ, прецизно изготвени документи и лична ангажираност — от първата консултация до неговото приключване.',
  "motto_labels": ["Подход", "Доверие", "Философия"],
  "panel": ["Свържете се с нас", "Първата стъпка е кратък разговор, в който изясняваме въпроса ви и възможните решения."],
  "quote": "Доверието се изгражда с последователна и отговорна работа. Ценим дългосрочните отношения с клиентите си и се гордеем, че много от тях работят с нас от години.",
  "slogans": ["Стремим се да познаваме в дълбочина дейността на всеки клиент, за да предложим решения, съобразени с неговите конкретни цели и интереси.",
              "Доверието се изгражда с последователна и отговорна работа. Ценим дългосрочните отношения с клиентите си и се гордеем, че много от тях работят с нас от години.",
              "Вярваме, че успехът е резултат от проактивност, добросъвестност и постоянство."],
  "stats": [("11", "области на бизнес правото"), ("2", "езика — български и английски"), ("1", "работен ден за отговор"), ("7", "партньорски компании")],
  "explore_more": "Към услугата",
  "statement": "Вярваме, че успехът е резултат от <strong>проактивно отношение</strong>, добра воля и постоянни усилия.",
  "about_eb": "За кантората",
  "about_h": "Посвещаваме времето, експертизата и усилията си на развитието на вашия бизнес",
  "about_p": ["SM Legal предоставя цялостно правно обслужване на бизнеса, основано на задълбочено познаване на дейността и целите на всеки клиент. Съпровождаме клиентите си от учредяването на дружеството през всеки етап на корпоративни промени и растеж.",
              "Работим с български и чуждестранни клиенти — основатели, инвеститори, собственици и управители на дружества."],
  "values": [("Проактивност", "Предвиждаме правните рискове и предлагаме решения, преди проблемът да е възникнал."),
             ("Задълбоченост", "Всяко становище се основава на внимателен анализ на фактите и на приложимото право."),
             ("Бизнес perspective", "Мислим в търговски категории и търсим решения, които са приложими на практика."),
             ("Прозрачност", "Ясни срокове, предвидимо възнаграждение и постоянна комуникация с клиента.")],
  "pr_eb": "Правни услуги", "pr_h": "Експертиза в единадесет области на бизнес правото",
  "pr_p": "Обединяваме корпоративна, регулаторна и процесуална експертиза, за да предложим на клиентите си цялостно правно обслужване.",
  "steps_eb": "Как работим", "steps_h": "Последователен процес — от първата консултация до приключването на възложената работа",
  "steps": [("Консултация", "Изслушваме ви, изясняваме целите и фактическата обстановка и очертаваме възможните варианти."),
            ("Анализ", "Проучваме документите и приложимото право и идентифицираме правните рискове."),
            ("Решение", "Предлагаме конкретен план за действие с ясни срокове и предварително договорено възнаграждение."),
            ("Подкрепа", "Изпълняваме възложената работа, представляваме ви пред трети лица и институции и оставаме на разположение и след приключването ѝ.")],
  "team_eb": "Екип", "team_p": "Специализира в търговското и корпоративното право, сделките с рисков капитал и интелектуалната собственост и има дългогодишен опит в работата с български и международни клиенти. Нейната мотивация за професионално развитие и желание да подкрепя клиентите в постигането на техните цели са довели до високо ниво на професионализъм, оценено положително от много клиенти.",
  "q_eb": "Препоръки", "q_h": "Отзиви на клиенти",
  "ins_eb": "Публикации", "ins_h": "Статии и новини", "ins_p": "Анализи на законодателни промени и практически насоки за бизнеса.",
  "partners_h": "Партньори и клиенти",
 },
 "en": {
  "title": "SM Legal — Marushkina Law Firm | Business Lawyer in Sofia, Bulgaria",
  "desc": "SM Legal is a business law firm in Sofia, Bulgaria: corporate and commercial law, venture capital, start-ups, employment and immigration, tax, compliance, GDPR, trade marks and disputes.",
  "eyebrow": "Law firm · Sofia, Bulgaria",
  "h1": "Legal solutions that keep your business <em>moving</em> forward",
  "lead": '<span class="brand-inline">SM Legal</span> provides legal services with close attention to detail and to each client’s specific objectives. Every matter receives thorough analysis, precisely drafted documentation and personal commitment — from the first consultation to its conclusion.',
  "motto_labels": ["Approach", "Trust", "Philosophy"],
  "panel": ["Get in touch", "The first step is a short conversation in which we clarify your question and the possible solutions."],
  "quote": "We are proud that years of hard work have brought excellent results, and our clients are still with us.",
  "slogans": ["We are here to understand your company's needs and offer you the best possible solutions.",
              "We are proud that years of hard work have brought excellent results, and our clients are still with us.",
              "We believe that success is the result of a proactive attitude, goodwill and constant effort."],
  "stats": [("11", "areas of business law"), ("2", "languages — Bulgarian and English"), ("1", "business day response time"), ("7", "partner companies")],
  "explore_more": "View practice area",
  "statement": "We believe that success is the result of a <strong>proactive attitude</strong>, goodwill and constant effort.",
  "about_eb": "About the firm",
  "about_h": "We dedicate our time, work and efforts to keep your business growing",
  "about_p": ["SM Legal aims to support your business entirely and to provide a wide spectrum of excellent legal services by understanding your business activity and goals. We support you in the incorporation process and during each stage of corporate change and growth.",
              "We work with Bulgarian and international clients — founders, investors, business owners and managers."],
  "values": [("Proactive", "We anticipate risks and propose solutions before problems arise."),
             ("Thorough", "Every opinion rests on careful analysis of the facts and the applicable law."),
             ("Business-minded", "We think in commercial terms and look for solutions that work in practice."),
             ("Transparent", "Clear timelines, predictable fees and constant communication.")],
  "pr_eb": "Practice areas", "pr_h": "Expertise across eleven areas of business law",
  "pr_p": "We combine corporate, regulatory and litigation expertise to offer our clients comprehensive legal support.",
  "steps_eb": "How we work", "steps_h": "A clear process from the first conversation to the result",
  "steps": [("Consultation", "We listen, clarify your goals and circumstances and outline the options."),
            ("Analysis", "We review the documents and applicable law and identify the risks."),
            ("Solution", "We propose a concrete plan with clear timelines and a fee agreed in advance."),
            ("Support", "We execute, represent you and remain available after completion.")],
  "team_eb": "Team", "team_p": "Specialises in commercial and corporate law, venture capital transactions and intellectual property, with long-standing experience working with Bulgarian and international clients. Her motivation for professional growth and eagerness to help clients achieve their goals have led to a high level of professionalism, positively assessed by many clients.",
  "q_eb": "Testimonials", "q_h": "What our clients say about us",
  "ins_eb": "Insights", "ins_h": "Articles and news", "ins_p": "Analysis of legislative changes and practical guidance for businesses.",
  "partners_h": "Partners and clients",
 },
}
HOME["bg"]["values"][2] = ("Бизнес мислене", HOME["bg"]["values"][2][1])

def build_home(lang):
    t = T[lang]; h = HOME[lang]
    path = ROUTES["home"][lang]; alt = ROUTES["home"]["en" if lang == "bg" else "bg"]
    out = head(lang, path, h["title"], h["desc"], alt, schema=[{"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "SM Legal", "inLanguage": ["bg", "en"], "publisher": {"@id": ORG_ID}}])
    out += header(lang, path, "home", alt)
    out += f"""<section class="hero"><div class="wrap hero__grid hero__grid--solo">
 <div class="hero__copy reveal"><span class="eyebrow">{h['eyebrow']}</span><h1>{h['h1']}</h1><p class="lead">{h['lead']}</p>
 <div class="hero__cta"><a class="btn" href="{rel(path, ROUTES['contact'][lang])}">{t['cta']}</a><a class="btn btn--ghost" href="{rel(path, ROUTES['practice'][lang])}">{t['all_practices']}</a></div></div>
</div></section>
<section class="mottos"><div class="wrap mottos__grid">{''.join(f'<figure class="motto reveal{" motto--dark" if i==1 else ""}"><figcaption>{esc(lbl)}</figcaption><blockquote>{esc(x)}</blockquote></figure>' for i,(lbl,x) in enumerate(zip(h['motto_labels'], h['slogans'])))}</div></section>
<section class="section"><div class="wrap grid-2">
 <div class="reveal"><span class="eyebrow">{h['about_eb']}</span><h2>{h['about_h']}</h2>{''.join('<p>'+esc(x)+'</p>' for x in h['about_p'])}
 <a class="link-arrow" href="{rel(path, ROUTES['about'][lang])}">{t['more']}</a></div>
 <div class="values reveal">{''.join(f'<div class="value"><h3>{esc(a)}</h3><p>{esc(b)}</p></div>' for a,b in h['values'])}</div>
</div></section>
<section class="section section--slate"><div class="wrap">
 <div class="sec-head"><span class="eyebrow">{h['steps_eb']}</span><h2>{h['steps_h']}</h2></div>
 <ol class="steps">{''.join(f'<li class="step reveal"><h3>{esc(a)}</h3><p>{esc(b)}</p></li>' for a,b in h['steps'])}</ol>
</div></section>
"""
    out += cta_band(lang, path) + footer(lang, path)
    emit(path, out, lang, alt)

def explorer(lang, path, more):
    tabs = []; panels = []
    for i, p in enumerate(PRACTICES):
        d = p[lang]; sel = i == 0
        tabs.append(f'<button type="button" role="tab" id="tab-{p["key"]}" aria-controls="pnl-{p["key"]}" aria-selected="{"true" if sel else "false"}" tabindex="{0 if sel else -1}"><span class="ex__n">{i+1:02d}</span>{esc(d["title"])}</button>')
        svc = "".join(f"<li>{esc(x)}</li>" for x in d["services"][:6])
        panels.append(f'<div class="ex__panel" role="tabpanel" id="pnl-{p["key"]}" aria-labelledby="tab-{p["key"]}"{"" if sel else " hidden"}>{icon(p["icon"], "ex__icon")}<h3>{esc(d["title"])}</h3><p>{esc(d["lead"])}</p><ul class="ex__list">{svc}</ul><a class="btn" href="{rel(path, practice_path(p["key"], lang))}">{more}</a></div>')
    return f'<div class="explorer reveal" data-explorer><div class="ex__tabs" role="tablist" aria-orientation="vertical">{"".join(tabs)}</div><div class="ex__panels">{"".join(panels)}</div></div>'

def slider(lang):
    slides = []
    for q in TESTIMONIALS:
        name = q["name_bg"] if lang == "bg" else q["name"]
        role = q["role_bg"] if lang == "bg" else q["role_en"]
        slides.append(f'<figure class="slide"><blockquote>{T[lang]["qo"]}{esc(q[lang])}{T[lang]["qc"]}</blockquote><figcaption><strong>{esc(name)}</strong><span>{esc(role)}</span></figcaption></figure>')
    prev, nxt = ("Предишна", "Следваща") if lang == "bg" else ("Previous", "Next")
    dots = "".join(f'<button type="button" aria-label="{i+1}"></button>' for i in range(len(slides)))
    return f'<div class="slider reveal" data-slider><div class="slider__viewport"><div class="slider__track">{"".join(slides)}</div></div><div class="slider__nav"><button type="button" class="slider__arrow" data-prev aria-label="{prev}">&larr;</button><div class="slider__dots">{dots}</div><button type="button" class="slider__arrow" data-next aria-label="{nxt}">&rarr;</button></div></div>'

def testimonial(q, lang):
    name = q["name_bg"] if lang == "bg" else q["name"]
    role = q["role_bg"] if lang == "bg" else q["role_en"]
    return f'<blockquote class="quote reveal"><p>{T[lang]['qo']}{esc(q[lang])}{T[lang]['qc']}</p><footer><strong>{esc(name)}</strong>{esc(role)}</footer></blockquote>'

CLIENTS = {
 "bg": {"eb": "Нашите клиенти", "h": "Български и международни дружества на всеки етап от тяхното развитие",
        "items": [("Стартъпи", "Основатели и млади екипи — от учредяването до привличането на първите инвестиции."),
                  ("Растящи компании (scale-up)", "Динамично развиващи се дружества, които навлизат на нови пазари и привличат капитал."),
                  ("Утвърдени компании", "Утвърдени дружества с текущи корпоративни, трудовоправни и регулаторни нужди.")]},
 "en": {"eb": "Our clients", "h": "Bulgarian and international companies at every stage of growth",
        "items": [("Start-ups", "Founders and young teams — from incorporation to the first investment rounds."),
                  ("Scale-ups", "Fast-growing businesses entering new markets and raising capital."),
                  ("Established companies", "Mature businesses with ongoing corporate, employment and regulatory needs.")]},
}
def clients_band(lang):
    c = CLIENTS[lang]
    items = "".join(f'<div class="client-type"><h3>{esc(a)}</h3><p>{esc(b)}</p></div>' for a, b in c["items"])
    return f'<section class="section section--tight"><div class="wrap"><div class="sec-head sec-head--center"><span class="eyebrow">{c["eb"]}</span><h2>{c["h"]}</h2></div><div class="client-types reveal">{items}</div></div></section>'

def partners(lang, path):
    lis = "".join(f'<li><img src="{rel(path, "assets/img/" + f)}" alt="{esc(n)}" onerror="var s=document.createElement(\'span\');s.textContent=this.alt;this.replaceWith(s)"></li>' for n, f in PARTNERS)
    return f'<ul class="partners">{lis}</ul>'

# ---- about
ABOUT = {
 "bg": {"title": "За нас | SM Legal — Адвокатско дружество Марушкина",
  "desc": "Запознайте се с SM Legal — адвокатска кантора в София с практика в бизнес правото: мисия, ценности и начин на работа с български и международни клиенти.",
  "h1": "За SM Legal", "sub": "Адвокатска кантора с практика в бизнес правото, която съпровожда своите клиенти на всеки етап от тяхното развитие.",
  "blocks": [
   ("Нашата мисия", ["SM Legal предоставя цялостно правно обслужване на бизнеса, основано на задълбочено познаване на дейността и целите на всеки клиент. Съпровождаме клиентите си от учредяването на дружеството през всеки етап на корпоративни промени и растеж."]),
   ("Кои са нашите клиенти", ["Работим с основатели на стартиращи и технологични компании, инвеститори и фондове за рисков капитал, малки и средни предприятия, чуждестранни дружества, които навлизат на българския пазар, както и с физически лица — предприемачи, управители и висококвалифицирани специалисти, които се установяват в България."]),
   ("Как работим", ["Всяко ангажиране започва с ясно определяне на предмета на възложената работа, сроковете и възнаграждението. Предлагаме почасово възнаграждение, фиксирано възнаграждение за определени услуги и абонаментно правно обслужване за клиенти с постоянни нужди."])],
  "facts": [("11", "области на бизнес правото"), ("2", "езика на обслужване — BG / EN"), ("1", "работен ден — срок за отговор"), ("100%", "фокус върху бизнеса")]},
 "en": {"title": "About Us | SM Legal — Marushkina Law Firm",
  "desc": "Meet SM Legal — a Sofia law firm focused on business law. Our mission, values and way of working with Bulgarian and international clients.",
  "h1": "About SM Legal", "sub": "A law firm built to support businesses at every stage of their development.",
  "blocks": [
   ("Our mission", ["SM Legal aims to support your business entirely and to provide a wide spectrum of excellent legal services by understanding your business activity and goals. We support you in the incorporation process and during each stage of corporate change and growth."]),
   ("Who our clients are", ["We work with founders of start-ups and technology companies, investors and venture capital funds, small and medium-sized enterprises, foreign companies entering the Bulgarian market, and individuals — entrepreneurs, managers and highly qualified professionals relocating to Bulgaria."]),
   ("How we work", ["Every engagement starts with a clear definition of the task, timeline and fees. We offer hourly rates, fixed fees for defined services and retainer arrangements for clients with ongoing needs."])],
  "facts": [("11", "areas of business law"), ("2", "working languages — BG / EN"), ("1", "business day response time"), ("100%", "business focus")]},
}
def build_about(lang):
    a = ABOUT[lang]; t = T[lang]; h = HOME[lang]
    path = ROUTES["about"][lang]; alt = ROUTES["about"]["en" if lang == "bg" else "bg"]
    hero, bc = page_hero(lang, path, [(a["h1"], path)], a["h1"], a["sub"])
    out = head(lang, path, a["title"], a["desc"], alt, schema=[bc, {"@type": "AboutPage", "url": url(path), "name": a["h1"], "about": {"@id": ORG_ID}}, person_schema(lang, path)])
    out += header(lang, path, "about", alt) + hero
    out += '<section class="section"><div class="wrap">'
    out += '<div class="about-cols">' + "".join(f'<article class="about-col reveal"><h2>{esc(hh)}</h2>{"".join("<p>"+esc(p)+"</p>" for p in ps)}</article>' for hh, ps in a["blocks"]) + '</div>'
    out += '</div></section>'
    out += team_block(lang, path)
    out += f'<section class="section section--sand"><div class="wrap"><div class="sec-head sec-head--center"><span class="eyebrow">{h["q_eb"]}</span><h2>{h["q_h"]}</h2></div>{slider(lang)}</div></section>'
    out += clients_band(lang)
    out += cta_band(lang, path) + footer(lang, path)
    emit(path, out, lang, alt)

# ---- practice index & pages
PR_INDEX = {
 "bg": {"title": "Правни услуги за бизнеса | SM Legal — адвокат в София",
        "desc": "Правни услуги на SM Legal: търговско и корпоративно право, рисков капитал, стартъпи и ИТ, трудово и имиграционно право, данъци и ДДС, корпоративно съответствие и AML, защита на личните данни, интелектуална собственост, недвижими имоти и спорове.",
        "h1": "Правни услуги", "sub": "Цялостно правно обслужване на бизнеса — от учредяването на дружеството и привличането на инвестиции до регулаторното съответствие и защитата на интересите на клиента при спорове."},
 "en": {"title": "Practice Areas | SM Legal — Business Lawyer in Sofia",
        "desc": "SM Legal practice areas: corporate and commercial law, venture capital, start-ups and technology, employment, immigration, tax and VAT, compliance and AML, GDPR, IP, real estate and disputes.",
        "h1": "Practice Areas", "sub": "Comprehensive legal support for businesses — from incorporation and investment to regulatory compliance and dispute resolution."},
}
AUDIENCES = {
 "companies": {"bg": "Компании", "en": "Companies", "keys": ["corporate", "employment", "tax", "compliance", "data", "ip", "realestate", "disputes"]},
 "founders":  {"bg": "Стартъпи и инвеститори", "en": "Start-ups & investors", "keys": ["vc", "startups", "corporate", "ip", "data", "tax"]},
 "foreign":   {"bg": "Чуждестранни клиенти", "en": "Foreign clients", "keys": ["immigration", "corporate", "tax", "realestate", "employment", "compliance"]},
}
PX = {
 "bg": {"for": "За кого", "all": "Всички области", "services": "Обхват на правната помощ", "faq": "Често задаван въпрос", "related": "Свързана публикация", "more": "Подробно за практиката", "of": "от", "prev": "Предишна област", "next": "Следваща област", "pick": "Изберете област"},
 "en": {"for": "Who it is for", "all": "All areas", "services": "What it covers", "faq": "Frequently asked", "related": "Further reading", "more": "Full practice area details", "of": "of", "prev": "Previous area", "next": "Next area", "pick": "Choose an area"},
}
def practice_hub(lang, path):
    t = T[lang]; x = PX[lang]; n = len(PRACTICES)
    chips = f'<button type="button" class="aud is-active" data-aud="all" aria-pressed="true">{x["all"]}</button>' + "".join(
        f'<button type="button" class="aud" data-aud="{k}" aria-pressed="false">{v[lang]}</button>' for k, v in AUDIENCES.items())
    tabs = []; panels = []
    for i, p in enumerate(PRACTICES):
        d = p[lang]; sel = i == 0; key = p["key"]
        auds = " ".join(k for k, v in AUDIENCES.items() if key in v["keys"])
        newb = f'<span class="hub__new">{t["new"]}</span>' if key in NEW_KEYS else ""
        tabs.append(f'<button type="button" role="tab" id="tab-{key}" data-key="{key}" data-aud="{auds}" aria-controls="pnl-{key}" aria-selected="{"true" if sel else "false"}" tabindex="{0 if sel else -1}">'
                    f'<span class="hub__n">{i+1:02d}</span><span class="hub__t">{esc(d["title"])}</span>{newb}</button>')
        svc = "".join(f"<li>{esc(s_)}</li>" for s_ in d["services"])
        q, ans = d["faq"][0]
        rel_posts = [y for y in sorted_posts() if y["practice"] == key]
        relh = ""
        if rel_posts:
            y = rel_posts[0]
            relh = f'<a class="hub__related" href="{rel(path, post_path(y, lang))}"><span>{x["related"]}</span>{esc(y[lang]["title"])}</a>'
        hidden = "" if sel else " hidden"
        panels.append(
            f'<article class="hub__panel" role="tabpanel" id="pnl-{key}" aria-labelledby="tab-{key}"{hidden}>'
            f'<header class="hub__head">{icon(p["icon"], "hub__icon")}<div><p class="hub__count">{i+1:02d} <span>{x["of"]} {n:02d}</span></p><h2>{esc(d["title"])}</h2></div></header>'
            f'<p class="hub__lead">{esc(d["lead"])}</p>'
            f'<div class="hub__body hub__body--stack"><div><h3>{x["services"]}</h3><ul class="hub__list hub__list--2">{svc}</ul></div>'
            f'<div class="hub__extra"><div class="hub__faq"><p class="hub__faq-l">{x["faq"]}</p><p class="hub__q">{esc(q)}</p><p>{esc(ans)}</p></div>{relh}</div></div>'
            f'<footer class="hub__foot"><div class="hub__cta"><a class="btn" href="{rel(path, practice_path(key, lang))}">{x["more"]}</a>'
            f'<a class="btn btn--ghost" href="{rel(path, ROUTES["contact"][lang])}">{t["cta"]}</a></div>'
            f'<div class="hub__steps"><button type="button" data-step="-1" aria-label="{x["prev"]}">&larr;</button><button type="button" data-step="1" aria-label="{x["next"]}">&rarr;</button></div></footer>'
            f'</article>')
    return (f'<div class="hub" data-hub><div class="hub__filter" role="group" aria-label="{x["for"]}"><span class="hub__label">{x["for"]}</span>{chips}</div>'
            f'<div class="hub__grid"><div class="hub__tabs" role="tablist" aria-orientation="vertical" aria-label="{x["pick"]}">{"".join(tabs)}</div>'
            f'<div class="hub__panels">{"".join(panels)}<div class="hub__bar" aria-hidden="true"><span></span></div></div></div></div>')


def build_practice_index(lang):
    a = PR_INDEX[lang]
    path = ROUTES["practice"][lang]; alt = ROUTES["practice"]["en" if lang == "bg" else "bg"]
    hero, bc = page_hero(lang, path, [(a["h1"], path)], a["h1"], a["sub"])
    il = {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": url(practice_path(p["key"], lang)), "name": p[lang]["title"]} for i, p in enumerate(PRACTICES)]}
    out = head(lang, path, a["title"], a["desc"], alt, schema=[bc, il])
    out += header(lang, path, "practice", alt) + hero
    out += f'<section class="section section--sand hub-section"><div class="wrap">{practice_hub(lang, path)}</div></section>'
    out += cta_band(lang, path) + footer(lang, path)
    emit(path, out, lang, alt)

def build_practice(p, lang):
    t = T[lang]; d = p[lang]
    path = practice_path(p["key"], lang); alt = practice_path(p["key"], "en" if lang == "bg" else "bg")
    idx = ROUTES["practice"][lang]
    hero, bc = page_hero(lang, path, [(PR_INDEX[lang]["h1"], idx), (d["title"], path)], d["title"], d["lead"], PR_INDEX[lang]["h1"])
    title = f'{d["title"]} | ' + ("Адвокат в София — SM Legal" if lang == "bg" else "Lawyer in Sofia — SM Legal")
    faq_schema = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d["faq"]]}
    svc_schema = {"@type": "Service", "name": d["title"], "serviceType": d["title"], "description": d["meta"], "provider": {"@id": ORG_ID},
                  "areaServed": {"@type": "Country", "name": "Bulgaria"}, "url": url(path),
                  "hasOfferCatalog": {"@type": "OfferCatalog", "name": d["title"], "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s}} for s in d["services"]]}}
    out = head(lang, path, title, d["meta"], alt, schema=[bc, svc_schema, faq_schema])
    out += header(lang, path, "practice", alt) + hero
    related = [x for x in sorted_posts() if x["practice"] == p["key"]]
    others = "".join(f'<li><a href="{rel(path, practice_path(o["key"], lang))}"{" aria-current=page" if o is p else ""}>{esc(o[lang]["title"])}</a></li>' for o in PRACTICES)
    rel_html = ""
    if related:
        rel_html = f'<div class="aside-box"><h3>{t["related"]}</h3><ul>' + "".join(f'<li><a href="{rel(path, post_path(x, lang))}">{esc(x[lang]["title"])}</a></li>' for x in related) + '</ul></div>'
    out += f"""<section class="section"><div class="wrap article-wrap">
<div class="prose">
 {''.join('<p>'+esc(x)+'</p>' for x in d['paras'])}
 <h2>{t['services']}</h2>
 <ul class="svc">{''.join('<li>'+esc(s)+'</li>' for s in d['services'])}</ul>
 <h2>{t['approach']}</h2>
 <p>{esc(d['approach'])}</p>
 <h2>{t['faq']}</h2>
 <div class="faq">{''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in d['faq'])}</div>
</div>
<aside class="aside">
 <div class="aside-box aside-box--dark"><h3>{t['cta_band_h']}</h3><p>{t['cta_band_p']}</p><a class="btn" href="{rel(path, ROUTES['contact'][lang])}">{t['cta']}</a></div>
 {rel_html}
 <div class="aside-box"><h3>{t['other_areas']}</h3><ul>{others}</ul></div>
</aside>
</div></section>"""
    out += cta_band(lang, path) + footer(lang, path)
    emit(path, out, lang, alt)

# ---- team
TEAM = {
 "bg": {"title": "Екип — адв. Силвия Марушкина | SM Legal",
  "desc": "Адвокат Силвия Марушкина — търговско и корпоративно право, венчър капитал, интелектуална собственост, имиграционно и трудово право. Основател на SM Legal, София.",
  "h1": "Екип", "sub": "Зад всяко решение стои личен ангажимент към успеха на клиента.",
  "bio": ["Адв. Силвия Марушкина има практика в областта на търговското и корпоративното право, сделките с рисков капитал и интелектуалната собственост и дългогодишен опит в работата с български и международни клиенти.",
          "Практиката ѝ обхваща учредяването и корпоративното обслужване на дружества, структурирането на инвестиционни сделки, регистрацията и защитата на търговски марки в България, в Европейския съюз и по Мадридската система, както и имиграционните и трудовоправните въпроси на компании, които привличат специалисти от чужбина.",
          "Към всеки възложен казус подхожда с прецизност, отговорност и лична ангажираност към интересите на клиента."],
  "focus": "Основни области", "langs_h": "Езици"},
 "en": {"title": "Team — Sylvia Marushkina, Attorney-at-law | SM Legal",
  "desc": "Sylvia Marushkina, attorney-at-law — corporate and commercial law, venture capital, intellectual property, immigration and employment law. Founder of SM Legal, Sofia.",
  "h1": "Team", "sub": "Behind every solution stands a personal commitment to the client's success.",
  "bio": ["Sylvia Marushkina specialises in commercial and corporate law, venture capital transactions and intellectual property, and has long-standing experience working with Bulgarian and international clients.",
          "Her practice covers company formation and corporate housekeeping, structuring investment transactions, registering and protecting trade marks in Bulgaria, the EU and under the Madrid System, as well as immigration and employment matters for companies hiring talent from abroad.",
          "Her motivation for professional growth and eagerness to help clients achieve their goals have led to a high level of professionalism, positively assessed by many clients."],
  "focus": "Key areas", "langs_h": "Languages"},
}
def person_schema(lang, path):
    t = T[lang]
    return {"@type": "Person", "@id": PERSON_ID, "name": t["author"], "jobTitle": t["author_role"], "worksFor": {"@id": ORG_ID},
            "knowsLanguage": ["bg", "en"], "knowsAbout": [P[k][lang]["title"] for k in ["corporate", "vc", "ip", "immigration", "employment"]],
            "image": SITE + "/assets/img/Sylvia-Marushkina-3.jpg", "url": url(path) + ("#ekip" if lang == "bg" else "#team")}

def team_block(lang, path):
    a = TEAM[lang]; t = T[lang]
    anchor = "ekip" if lang == "bg" else "team"
    tags = "".join(f'<li><a href="{rel(path, practice_path(k, lang))}">{esc(P[k][lang]["title"])}</a></li>' for k in ["corporate", "vc", "startups", "ip", "immigration", "employment"])
    return f"""<section class="section section--white" id="{anchor}"><div class="wrap grid-2 grid-2--top">
 <div class="portrait reveal"><img src="{rel(path, 'assets/img/Sylvia-Marushkina-3.jpg')}" alt="{t['author']}" width="640" height="800" loading="lazy" onerror="this.remove()"></div>
 <div class="reveal"><span class="eyebrow">{a['h1']}</span><p class="role">{t['author_role']}</p><h2>{t['author']}</h2>
 {''.join('<p>'+esc(x)+'</p>' for x in a['bio'])}
 <h3 style="margin-top:30px">{a['focus']}</h3><ul class="tags">{tags}</ul>
 <div class="hero__cta"><a class="btn" href="{rel(path, ROUTES['contact'][lang])}">{t['cta']}</a><a class="btn btn--ghost" href="mailto:{EMAIL}">{EMAIL}</a></div></div>
</div></section>"""

# ---- insights
INS = {
 "bg": {"title": "Публикации — статии и новини | SM Legal",
        "desc": "Правни анализи и новини от SM Legal: законодателни промени и практически насоки в областта на търговското право, рисковия капитал, имиграцията, корпоративното съответствие и интелектуалната собственост.",
        "h1": "Публикации", "sub": "Анализи, практически насоки и новини за законодателни промени, които засягат вашия бизнес."},
 "en": {"title": "Insights — Articles and News | SM Legal",
        "desc": "Legal articles and news from SM Legal: legislative updates and practical guidance on Bulgarian corporate law, venture capital, immigration, compliance and intellectual property.",
        "h1": "Insights", "sub": "Articles, analysis and news on legislative changes that affect your business."},
}
def build_insights_index(lang):
    a = INS[lang]; t = T[lang]
    path = ROUTES["insights"][lang]; alt = ROUTES["insights"]["en" if lang == "bg" else "bg"]
    hero, bc = page_hero(lang, path, [(a["h1"], path)], a["h1"], a["sub"])
    blog = {"@type": "Blog", "name": a["h1"] + " — SM Legal", "url": url(path), "inLanguage": lang, "publisher": {"@id": ORG_ID},
            "blogPost": [{"@type": "BlogPosting", "headline": x[lang]["title"], "url": url(post_path(x, lang)), "datePublished": x["date"]} for x in sorted_posts()]}
    out = head(lang, path, a["title"], a["desc"], alt, schema=[bc, blog])
    out += header(lang, path, "insights", alt) + hero
    used = []
    for x in sorted_posts():
        if x["practice"] not in used: used.append(x["practice"])
    fbtn = f'<button type="button" data-filter="all" aria-pressed="true">{t["filter_all"]}</button><button type="button" data-filter="news" aria-pressed="false">{t["filter_news"]}</button><button type="button" data-filter="article" aria-pressed="false">{t["filter_articles"]}</button>'
    fbtn += "".join(f'<button type="button" data-filter="{k}" aria-pressed="false">{esc(P[k][lang]["title"])}</button>' for k in used)
    out += f'<section class="section"><div class="wrap"><div class="filters" role="toolbar">{fbtn}</div><div class="posts">{"".join(post_card(x, lang, path) for x in sorted_posts())}</div></div></section>'
    out += cta_band(lang, path) + footer(lang, path)
    emit(path, out, lang, alt)

def build_post(x, lang):
    t = T[lang]; d = x[lang]
    path = post_path(x, lang); alt = post_path(x, "en" if lang == "bg" else "bg")
    idx = ROUTES["insights"][lang]
    typ = t["news"] if x["type"] == "news" else t["article"]
    c, bc = crumbs(lang, path, [(INS[lang]["h1"], idx), (d["title"], path)])
    art = {"@type": "NewsArticle" if x["type"] == "news" else "Article", "headline": d["title"], "description": d["excerpt"],
           "datePublished": x["date"], "dateModified": x["date"], "inLanguage": lang, "mainEntityOfPage": url(path),
           "image": SITE + "/assets/img/og-image.png", "author": {"@id": PERSON_ID, "@type": "Person", "name": t["author"]},
           "publisher": {"@id": ORG_ID}, "about": P[x["practice"]][lang]["title"]}
    # optional per-post SEO overrides and FAQ block (rendered separately, with FAQPage schema)
    schema = [bc, art]
    faq_html = ""
    if d.get("faq"):
        schema.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d["faq"]]})
        faq_html = f'<h2>{esc(d.get("faq_title", t["faq"]))}</h2>\n<div class="faq">' + "".join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in d["faq"]) + '</div>\n'
    out = head(lang, path, d.get("seo_title", d["title"]) + " | SM Legal", d.get("seo_desc", d["excerpt"]), alt, og_type="article", schema=schema)
    out += header(lang, path, "insights", alt)
    out += '<div class="read-progress" aria-hidden="true"><span></span></div>'
    out += f"""<section class="page-hero dark"><div class="wrap">{c}
<div class="post__meta" style="color:#bdb8b1"><span class="badge">{typ}</span><time datetime="{x['date']}">{fmt_date(x['date'], lang)}</time><span>{x['read']} {t['min']}</span></div>
<h1>{esc(d['title'])}</h1><p>{esc(d['excerpt'])}</p></div></section>"""
    others = [y for y in sorted_posts() if y is not x][:3]
    pr = P[x["practice"]]
    out += f"""<section class="section"><div class="wrap article-wrap">
<article class="prose{' prose--darkh' if x.get('dark_headings') else ''}">{d['body']}
{faq_html}<p class="disclaimer">{t['disclaimer']}</p>
<p style="font-size:.9rem;color:var(--muted)"><strong style="color:var(--ink)">{t['author']}</strong> — {t['author_role']}</p></article>
<aside class="aside">
 <div class="aside-box aside-box--dark"><h3>{t['cta_band_h']}</h3><p>{t['cta_band_p']}</p><a class="btn" href="{rel(path, ROUTES['contact'][lang])}">{t['cta']}</a></div>
 <div class="aside-box"><h3>{esc(pr[lang]['title'])}</h3><p style="font-size:.92rem;color:var(--muted)">{esc(pr[lang]['short'])}</p><a class="link-arrow" href="{rel(path, practice_path(pr['key'], lang))}">{t['more']}</a></div>
</aside></div></section>
<section class="section section--white"><div class="wrap"><div class="sec-head"><span class="eyebrow">{t['related']}</span></div><div class="posts">{''.join(post_card(y, lang, path) for y in others)}</div></div></section>"""
    out += footer(lang, path)
    emit(path, out, lang, alt, lastmod=x["date"])

# ---- contact
CONTACT = {
 "bg": {"title": "Контакти — заявете консултация | SM Legal, София",
  "desc": "Свържете се с адвокатска кантора SM Legal в София, ул. „Добротица Деспот“ 41. Заявете консултация по търговско и корпоративно, трудово, имиграционно право и други области на бизнес правото.",
  "h1": "Контакти", "sub": "Опишете накратко въпроса си и ще се свържем с вас в рамките на един работен ден. Всяка предоставена ни информация се ползва със закрилата на адвокатската тайна.",
  "form_h": "Заявка за консултация",
  "mail_p": "Изпратете ни кратко описание на въпроса си — ще получите отговор в рамките на един работен ден. За по-бърза оценка посочете:",
  "mail_list": ["кратко описание на казуса и желания резултат;", "засегнатите държави или компании;", "срокове, ако има такива;", "телефон за обратна връзка (по желание)."],
  "mail_btn": "Пишете ни на имейл", "mail_subj": "Запитване за консултация",
  "mail_body": "Здравейте,\n\nБих искал/а консултация по следния въпрос:\n\n\nИме:\nКомпания:\nТелефон:\n",
  "mail_note": "Бутонът отваря вашата пощенска програма. Данните, които ни изпращате, се обработват съгласно",
  "copy": "Копирай адреса", "copied": "Адресът е копиран",
  "map": "Вижте на картата"},
 "en": {"title": "Contact — Request a Consultation | SM Legal, Sofia",
  "desc": "Contact SM Legal law firm in Sofia, Bulgaria — 41 Dobrotitsa Despot Str. Request a consultation on corporate, employment, immigration law and more.",
  "h1": "Contact", "sub": "Briefly describe your question and we will get back to you within one business day.",
  "form_h": "Consultation request",
  "mail_p": "Send us a short description of your question and we will reply within one business day. To help us assess it quickly, please include:",
  "mail_list": ["a brief summary of the matter and the outcome you seek;", "the countries or companies involved;", "any deadlines;", "a phone number for a call back (optional)."],
  "mail_btn": "Email us", "mail_subj": "Consultation request",
  "mail_body": "Hello,\n\nI would like a consultation on the following matter:\n\n\nName:\nCompany:\nPhone:\n",
  "mail_note": "The button opens your email app. Any data you send us is processed in accordance with the",
  "copy": "Copy address", "copied": "Address copied",
  "map": "View on map"},
}
def build_contact(lang):
    a = CONTACT[lang]; t = T[lang]
    path = ROUTES["contact"][lang]; alt = ROUTES["contact"]["en" if lang == "bg" else "bg"]
    hero, bc = page_hero(lang, path, [(a["h1"], path)], a["h1"], a["sub"])
    out = head(lang, path, a["title"], a["desc"], alt, schema=[bc, {"@type": "ContactPage", "url": url(path), "about": {"@id": ORG_ID}}])
    out += header(lang, path, "contact", alt) + hero
    from urllib.parse import quote
    mailto = f"mailto:{EMAIL}?subject={quote(a['mail_subj'])}&amp;body={quote(a['mail_body'])}"
    maps = "https://www.google.com/maps/search/?api=1&query=" + "Dobrotitsa+Despot+41,+Sofia+1612"
    out += f"""<section class="section"><div class="wrap contact-grid">
<div class="reveal">
 <ul class="info-list">
  <li>{icon('pin')}<div><strong>{t['address_l']}</strong>{t['address']}<br><a class="link-arrow" href="{maps}" target="_blank" rel="noopener">{a['map']}</a></div></li>
  <li>{icon('mail')}<div><strong>{t['email_l']}</strong><a href="mailto:{EMAIL}">{EMAIL}</a></div></li>
  <li>{icon('clock')}<div><strong>{t['hours_l']}</strong>{t['hours']}</div></li>
 </ul>
</div>
<div class="form mail-panel reveal">
 <h2 style="font-size:2rem">{a['form_h']}</h2>
 <p>{a['mail_p']}</p>
 <ul class="mail-list">{''.join(f'<li>{esc(i)}</li>' for i in a['mail_list'])}</ul>
 <div class="mail-actions">
  <a class="btn" href="{mailto}">{icon('mail')}<span>{a['mail_btn']}</span></a>
  <button type="button" class="btn btn--ghost" data-copy="{EMAIL}" data-copied="{esc(a['copied'])}">{a['copy']}</button>
 </div>
 <p class="mail-addr"><a href="mailto:{EMAIL}">{EMAIL}</a></p>
 <p class="form-note-s">{a['mail_note']} <a href="{rel(path, ROUTES['privacy'][lang])}">{t['privacy'].lower()}</a>.</p>
</div>
</div></section>"""
    out += footer(lang, path)
    emit(path, out, lang, alt)

# ---- privacy
PRIV = {
 "bg": {"title": "Политика за поверителност | SM Legal", "h1": "Политика за поверителност",
  "desc": "Политика за поверителност на SM Legal — как обработваме личните данни, предоставени чрез уебсайта smlegal.bg.",
  "body": """<p>Настоящата политика описва начина, по който SM Legal — Адвокатско дружество Марушкина („ние“), обработва личните данни на посетителите на уебсайта smlegal.bg и на лицата, които се свързват с нас.</p>
<h2>Администратор на данните</h2><p>Адвокат Силвия Марушкина, адрес: гр. София 1612, ул. „Добротица Деспот“ № 41, електронна поща: smarushkina@smlegal.bg.</p>
<h2>Какви данни обработваме</h2><p>Обработваме данните, които ни предоставяте по електронна поща или по телефон — име, адрес на електронна поща, телефон, наименование на дружеството и съдържанието на съобщението. Уебсайтът не съдържа форми за въвеждане на лични данни.</p><p>При посещение на уебсайта хостинг доставчикът автоматично обработва техническа информация (IP адрес, вид на браузъра, дата и час на заявката), необходима за предоставянето и сигурността на уебсайта.</p>
<h2>Цели и правно основание</h2><ul><li>отговор на вашето запитване и предприемане на стъпки преди сключването на договор за правна защита и съдействие — чл. 6, пар. 1, буква „б“ от Регламент (ЕС) 2016/679 (GDPR);</li><li>изпълнение на законови задължения, включително по Закона за адвокатурата и Закона за мерките срещу изпирането на пари — чл. 6, пар. 1, буква „в“ от GDPR;</li><li>законен интерес от сигурното и надеждно функциониране на уебсайта — чл. 6, пар. 1, буква „е“ от GDPR;</li><li>съгласие — по отношение на аналитичните бисквитки, ако бъдат използвани — чл. 6, пар. 1, буква „а“ от GDPR.</li></ul>
<h2>Срок на съхранение</h2><p>Данните от запитвания, които не са довели до сключване на договор, се съхраняват за срок до 12 месеца. Данните на клиентите се съхраняват в сроковете, предвидени в приложимото законодателство.</p>
<h2>Получатели</h2><p>Не предоставяме личните ви данни на трети лица, освен на доставчици на хостинг и имейл услуги, които действат като обработващи лични данни по наше възлагане, или когато това се изисква по закон. Уебсайтът се хоства от GitHub Pages (GitHub, Inc., САЩ); предаването на данни към САЩ се основава на Рамката за защита на данните между ЕС и САЩ и/или на стандартни договорни клаузи. Адвокатската тайна се спазва при всички обстоятелства.</p>
<h2 id="cookies">Бисквитки</h2><p>Бисквитките са малки текстови файлове, които се съхраняват в браузъра ви. Уебсайтът не използва рекламни бисквитки. Шрифтовете се зареждат директно от нашия уебсайт, без заявки към външни услуги.</p><ul><li><strong>Необходими</strong> — запис в браузъра ви (localStorage, ключ „sm_cookie_consent“), който съхранява избора ви относно бисквитките за срок до 12 месеца. Не изисква съгласие.</li><li><strong>Аналитични</strong> — Google Analytics (Google Ireland Ltd.), за анонимизирана статистика на посещенията. Зареждат се единствено ако изрично ги приемете; срок на съхранение до 14 месеца.</li></ul><p>Можете да промените или оттеглите съгласието си по всяко време чрез връзката „Настройки за бисквитки“ в долната част на всяка страница или като изтриете бисквитките чрез настройките на браузъра си.</p>
<h2>Вашите права</h2><p>Имате право на достъп до личните си данни, на тяхното коригиране и изтриване, на ограничаване на обработването, на преносимост и на възражение, както и право да оттеглите съгласието си по всяко време, без това да засяга законосъобразността на обработването преди оттеглянето. Можете да упражните правата си, като ни пишете на smarushkina@smlegal.bg. Имате право да подадете жалба до Комисията за защита на личните данни (www.cpdp.bg).</p>
<p><em>Последна актуализация: ноември 2026 г.</em></p>"""},
 "en": {"title": "Privacy Policy | SM Legal", "h1": "Privacy Policy",
  "desc": "SM Legal privacy policy — how we process personal data submitted through the smlegal.bg website.",
  "body": """<p>This policy explains how SM Legal — Marushkina Law Firm ("we") processes the personal data of visitors to smlegal.bg and of persons who contact us.</p>
<h2>Data controller</h2><p>Attorney-at-law Sylvia Marushkina, 41 Dobrotitsa Despot Str., Sofia 1612, Bulgaria, email: smarushkina@smlegal.bg.</p>
<h2>Data we process</h2><p>We process the data you provide by email or by phone — name, email address, phone number, company name and the content of your message. The website contains no forms for entering personal data.</p><p>When you visit the website, the hosting provider automatically processes technical information (IP address, browser type, date and time of the request) needed to deliver and secure the site.</p>
<h2>Purposes and legal basis</h2><ul><li>responding to your enquiry and taking steps prior to entering into an engagement — Art. 6(1)(b) of Regulation (EU) 2016/679 (GDPR);</li><li>compliance with legal obligations, including under the Bar Act and anti-money laundering legislation — Art. 6(1)(c) GDPR;</li><li>our legitimate interest in the secure and reliable operation of the website — Art. 6(1)(f) GDPR;</li><li>consent — for analytics cookies, if enabled — Art. 6(1)(a) GDPR.</li></ul>
<h2>Retention</h2><p>Data from enquiries that do not result in an engagement are kept for up to 12 months. Client data are kept for the periods required by applicable law.</p>
<h2>Recipients</h2><p>We do not disclose your data to third parties, except to hosting and email service providers acting on our behalf, or where required by law. The website is hosted by GitHub Pages (GitHub, Inc., USA); transfers to the USA rely on the EU–U.S. Data Privacy Framework and/or standard contractual clauses. Attorney–client privilege is observed at all times.</p>
<h2 id="cookies">Cookies</h2><p>Cookies are small files stored in your browser. This website does not use advertising cookies. Fonts are served directly from our own site, with no requests to external services.</p><ul><li><strong>Necessary</strong> — a browser storage entry (localStorage, key “sm_cookie_consent”) that remembers your cookie choice for up to 12 months. No consent required.</li><li><strong>Analytics</strong> — Google Analytics (Google Ireland Ltd.), providing anonymised visit statistics. Loaded only if you expressly accept them; retention up to 14 months.</li></ul><p>You can change or withdraw your consent at any time via the “Cookie settings” link at the bottom of every page, or by deleting cookies in your browser settings.</p>
<h2>Your rights</h2><p>You have the right of access, rectification, erasure, restriction of processing, data portability and objection, and the right to withdraw consent at any time. You may exercise your rights by writing to smarushkina@smlegal.bg. You also have the right to lodge a complaint with the Commission for Personal Data Protection (www.cpdp.bg).</p>
<p><em>Last updated: November 2026</em></p>"""},
}
def build_privacy(lang):
    a = PRIV[lang]
    path = ROUTES["privacy"][lang]; alt = ROUTES["privacy"]["en" if lang == "bg" else "bg"]
    hero, bc = page_hero(lang, path, [(a["h1"], path)], a["h1"], "")
    out = head(lang, path, a["title"], a["desc"], alt, schema=[bc])
    out += header(lang, path, "", alt) + hero
    out += f'<section class="section"><div class="wrap"><div class="prose" style="max-width:820px">{a["body"]}</div></div></section>'
    out += footer(lang, path)
    emit(path, out, lang, alt)

def build_404():
    path = "404.html"
    out = head("bg", path, "Страницата не е намерена | SM Legal", "Страницата не е намерена.", None, noindex=True)
    out += header("bg", path, "", None)
    out += f"""<section class="page-hero dark" style="padding:120px 0"><div class="wrap"><span class="eyebrow">404</span>
<h1>Страницата не е намерена</h1><p>Страницата, която търсите, е преместена или не съществува. / The page you are looking for may have been moved or no longer exists.</p>
<div class="hero__cta" style="margin-top:30px"><a class="btn" href="/">Начало</a><a class="btn btn--ghost" href="/en/">Home (EN)</a></div></div></section>"""
    out += footer("bg", path)
    out = out.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<base href="/">', 1)
    emit(path, out, sitemap=False)

# ---------------------------------------------------------------- write
def write_all():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    # static assets live in the repository root (assets/)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"))
    for lang in ("bg", "en"):
        build_home(lang); build_about(lang); build_practice_index(lang)
        build_insights_index(lang); build_contact(lang); build_privacy(lang)
        for p in PRACTICES: build_practice(p, lang)
        for x in INSIGHTS: build_post(x, lang)
    build_404()
    for pg in PAGES:
        fp = os.path.join(OUT, pg["path"])
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, "w", encoding="utf-8") as f:
            f.write(pg["html"])
    # sitemap
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for pg in PAGES:
        if not pg["sitemap"]: continue
        sm.append(f' <url><loc>{url(pg["path"])}</loc><lastmod>{pg["lastmod"]}</lastmod>')
        if pg["alt"]:
            bgp = pg["path"] if pg["lang"] == "bg" else pg["alt"]
            enp = pg["path"] if pg["lang"] == "en" else pg["alt"]
            sm.append(f'  <xhtml:link rel="alternate" hreflang="bg" href="{url(bgp)}"/>')
            sm.append(f'  <xhtml:link rel="alternate" hreflang="en" href="{url(enp)}"/>')
            sm.append(f'  <xhtml:link rel="alternate" hreflang="x-default" href="{url(bgp)}"/>')
        sm.append(' </url>')
    sm.append('</urlset>')
    open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(sm))
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    # GitHub Pages: custom domain + no Jekyll processing
    open(os.path.join(OUT, "CNAME"), "w").write(SITE.split("//")[1] + "\n")
    open(os.path.join(OUT, ".nojekyll"), "w").write("")
    # former Team pages -> About (GitHub Pages has no server-side redirects)
    for old, new in (("ekip.html", "za-nas.html#ekip"), ("en/team.html", "en/about.html#team")):
        target = url(new)
        os.makedirs(os.path.dirname(os.path.join(OUT, old)) or OUT, exist_ok=True)
        open(os.path.join(OUT, old), "w", encoding="utf-8").write(
            f'<!doctype html><html><head><meta charset="utf-8"><title>SM Legal</title>'
            f'<meta name="robots" content="noindex"><link rel="canonical" href="{target}">'
            f'<meta http-equiv="refresh" content="0; url={target}"></head>'
            f'<body><a href="{target}">{target}</a></body></html>\n')
    print(len(PAGES), "pages")

def publish():
    """Copy the built site from dist/ to the repository root (served by GitHub Pages)."""
    for name in os.listdir(OUT):
        src, dst = os.path.join(OUT, name), os.path.join(ROOT, name)
        if os.path.isdir(src):
            if os.path.exists(dst): shutil.rmtree(dst)
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
    shutil.rmtree(OUT)
    print("published to", ROOT)

if __name__ == "__main__":
    import sys
    write_all()
    if "--publish" in sys.argv:
        publish()
