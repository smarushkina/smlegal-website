# -*- coding: utf-8 -*-
"""Static site generator for SM Legal (smlegal.bg). Run: python3 build.py"""
import os, json, shutil, html, datetime, posixpath
from content_practice1 import PRACTICES_1
from content_practice2 import PRACTICES_2
from content_insights import INSIGHTS

SITE = "https://smlegal.bg"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")
PRACTICES = PRACTICES_1 + PRACTICES_2
NEW_KEYS = {"startups", "tax", "compliance"}
EMAIL = "office@smlegal.bg"
TODAY = datetime.date(2026, 10, 6).isoformat()
P = {p["key"]: p for p in PRACTICES}
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
  "brand_sub": "Адвокатска кантора Марушкина",
  "nav": [("home","Начало"),("about","За нас"),("practice","Правни услуги"),("insights","Публикации"),("contact","Контакти")],
  "cta": "Заявете консултация", "more": "Научете повече", "read": "Прочетете", "all_practices": "Всички правни услуги",
  "all_posts": "Всички публикации", "news": "Новина", "article": "Статия", "min": "мин. четене",
  "services": "Нашите услуги", "approach": "Нашият подход", "faq": "Често задавани въпроси", "other_areas": "Други правни услуги",
  "related": "Свързани публикации", "new": "Ново", "address": "ул. „Добротица Деспот“ 41, София 1612",
  "address_l": "Адрес", "email_l": "Имейл", "hours_l": "Работно време", "hours": "Понеделник – петък, 9:30 – 18:00 ч.",
  "langs_l": "Езици на обслужване", "langs": "български, английски",
  "foot_about": "Ние посвещаваме времето, работата и усилията си, за да продължава вашият бизнес да расте.",
  "foot_practices": "Правни услуги", "foot_firm": "Кантората", "foot_visit": "Посетете ни",
  "rights": "Всички права запазени.", "privacy": "Политика за поверителност",
  "disclaimer": "Публикацията има информационен характер и не представлява правна консултация. За съвет относно конкретен случай, моля, свържете се с нас.",
  "home_l": "Начало", "skip": "Към съдържанието", "menu": "Меню", "back_top": "Към началото",
  "cta_band_h": "Нуждаете се от правен съвет?",
  "cta_band_p": "Свържете се с нас — ще отговорим в рамките на един работен ден.",
  "filter_all": "Всички", "filter_news": "Новини", "filter_articles": "Статии",
  "author": "Силвия Марушкина", "author_role": "Адвокат, основател на SM Legal",
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
     "name": "SM Legal — Marushkina Law Firm", "alternateName": ["SM Legal", "Адвокатска кантора Марушкина"],
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
    css = rel(path, "assets/css/style.css")
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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@200;300;400&family=Raleway:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap">
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
    pr = "".join(f'<li><a href="{rel(path, practice_path(p["key"], lang))}">{esc(p[lang]["title"])}</a></li>' for p in PRACTICES[:6])
    pr2 = "".join(f'<li><a href="{rel(path, practice_path(p["key"], lang))}">{esc(p[lang]["title"])}</a></li>' for p in PRACTICES[6:])
    firm = "".join(f'<li><a href="{rel(path, ROUTES[k][lang])}">{l}</a></li>' for k, l in t["nav"] if k != "home")
    firm += f'<li><a href="{rel(path, ROUTES["privacy"][lang])}">{t["privacy"]}</a></li>'
    return f"""</main>
<footer class="site-footer">
 <div class="wrap">
  <div class="foot-grid">
   <div>
    {logo(rel(path, ROUTES['home'][lang]), variant='logo-rose').replace('{LOGO_PREFIX}', rel(path, 'x')[:-1])}
    <p>{t['foot_about']}</p>
    <p>{t['address']}<br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
   </div>
   <div><h4>{t['foot_practices']}</h4><ul>{pr}</ul></div>
   <div><h4>&nbsp;</h4><ul>{pr2}</ul></div>
   <div><h4>{t['foot_firm']}</h4><ul>{firm}</ul></div>
  </div>
  <div class="foot-bottom"><span>© 2026 SM Legal — {t['brand_sub']}. {t['rights']}</span><a href="{rel(path, ROUTES['privacy'][lang])}">{t['privacy']}</a></div>
 </div>
</footer>
<a class="to-top" href="#main" aria-label="{t['back_top']}">{icon('up')}</a>
<script src="{rel(path, 'assets/js/main.js')}" defer></script>
</body>
</html>
"""

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
  "title": "SM Legal — Адвокатска кантора Марушкина | Бизнес адвокат в София",
  "desc": "SM Legal е адвокатска кантора в София за бизнеса: търговско и корпоративно право, венчър капитал, стартъпи, трудово и имиграционно право, данъци, compliance, GDPR, търговски марки и спорове.",
  "eyebrow": "Адвокатска кантора · София",
  "h1": "Правни решения, които <em>движат</em> бизнеса ви напред",
  "lead": "Адвокатска кантора за бизнеса в София. Съветваме компании, основатели и инвеститори по търговско и корпоративно право, инвестиции, имиграция и регулаторно съответствие — на български и английски език.",
  "motto_labels": ["Подход", "Доверие", "Философия"],
  "panel": ["Свържете се с нас", "Първата стъпка е кратък разговор, в който изясняваме въпроса ви и възможните решения."],
  "quote": "Гордеем се, че с години упорит труд постигнахме отлични резултати, а клиентите ни остават с нас.",
  "slogans": ["Тук сме, за да разберем нуждите на вашата компания и да ви предложим най-добрите възможни решения.",
              "Гордеем се, че с години упорит труд постигнахме отлични резултати, а клиентите ни остават с нас.",
              "Вярваме, че успехът е резултат от проактивно отношение, добра воля и постоянни усилия."],
  "stats": [("11", "области на бизнес правото"), ("2", "езика — български и английски"), ("1", "работен ден за отговор"), ("7", "партньорски компании")],
  "explore_more": "Към услугата",
  "statement": "Вярваме, че успехът е резултат от <strong>проактивно отношение</strong>, добра воля и постоянни усилия.",
  "about_eb": "За кантората",
  "about_h": "Посвещаваме времето, работата и усилията си, за да расте вашият бизнес",
  "about_p": ["SM Legal има за цел да подкрепя бизнеса ви изцяло и да предоставя широк спектър от отлични правни услуги, като разбира вашата дейност и цели. Подкрепяме ви в процеса на учредяване на компанията и на всеки етап от корпоративните промени и растежа.",
              "Работим с български и международни клиенти — основатели, инвеститори, собственици на бизнес и мениджъри — на български и английски език."],
  "values": [("Проактивност", "Предвиждаме рисковете и предлагаме решения, преди проблемът да възникне."),
             ("Задълбоченост", "Всяко становище стъпва на внимателен анализ на фактите и на приложимото право."),
             ("Бизнес perspective", "Мислим в търговски категории и търсим решения, които работят на практика."),
             ("Прозрачност", "Ясни срокове, предвидими разходи и постоянна комуникация с клиента.")],
  "pr_eb": "Правни услуги", "pr_h": "Експертиза в единадесет области на бизнес правото",
  "pr_p": "Обединяваме корпоративна, регулаторна и процесуална експертиза, за да предложим на клиентите си цялостно правно обслужване.",
  "steps_eb": "Как работим", "steps_h": "Ясен процес от първия разговор до резултата",
  "steps": [("Консултация", "Изслушваме ви, изясняваме целите и обстоятелствата и очертаваме възможните варианти."),
            ("Анализ", "Проучваме документите и приложимото право и идентифицираме рисковете."),
            ("Решение", "Предлагаме конкретен план с ясни срокове и предварително договорено възнаграждение."),
            ("Подкрепа", "Изпълняваме, представляваме ви и оставаме на разположение и след приключването.")],
  "team_eb": "Екип", "team_p": "Специализира в търговското и корпоративното право, сделките с рисков капитал и интелектуалната собственост и има дългогодишен опит в работата с български и международни клиенти. Нейната мотивация за професионално развитие и желание да подкрепя клиентите в постигането на техните цели са довели до високо ниво на професионализъм, оценено положително от много клиенти.",
  "q_eb": "Препоръки", "q_h": "Какво казват клиентите ни",
  "ins_eb": "Публикации", "ins_h": "Статии и новини", "ins_p": "Анализи на законодателни промени и практически насоки за бизнеса.",
  "partners_h": "Партньори и клиенти",
 },
 "en": {
  "title": "SM Legal — Marushkina Law Firm | Business Lawyer in Sofia, Bulgaria",
  "desc": "SM Legal is a business law firm in Sofia, Bulgaria: corporate and commercial law, venture capital, start-ups, employment and immigration, tax, compliance, GDPR, trade marks and disputes.",
  "eyebrow": "Law firm · Sofia, Bulgaria",
  "h1": "Legal solutions that keep your business <em>moving</em> forward",
  "lead": "A business law firm in Sofia. We advise companies, founders and investors on corporate and commercial law, investment, immigration and regulatory compliance — in Bulgarian and English.",
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
              "We work with Bulgarian and international clients — founders, investors, business owners and managers — in Bulgarian and English."],
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
    out += f"""<section class="hero"><div class="wrap hero__grid">
 <div class="hero__copy reveal"><span class="eyebrow">{h['eyebrow']}</span><h1>{h['h1']}</h1><p class="lead">{h['lead']}</p>
 <div class="hero__cta"><a class="btn" href="{rel(path, ROUTES['contact'][lang])}">{t['cta']}</a><a class="btn btn--ghost" href="{rel(path, ROUTES['practice'][lang])}">{t['all_practices']}</a></div></div>
 <aside class="hero__panel" aria-label="{h['panel'][0]}">
  <img class="hero__logo" src="{rel(path, 'assets/img/brand/logo-rose.svg')}" alt="" width="551" height="220">
  <div class="hero__contact">
   <p class="hero__contact-h">{h['panel'][0]}</p>
   <p class="hero__contact-p">{h['panel'][1]}</p>
   <ul>
    <li>{icon('pin')}<span>{t['address']}</span></li>
    <li>{icon('mail')}<a href="mailto:{EMAIL}">{EMAIL}</a></li>
    <li>{icon('clock')}<span>{t['hours']}</span></li>
   </ul>
  </div>
 </aside>
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
 "bg": {"eb": "Нашите клиенти", "h": "Български и международни компании на всеки етап от развитието си",
        "items": [("Стартъпи", "Основатели и млади екипи — от учредяването до първите инвестиции."),
                  ("Scale-up компании", "Бързо растящи бизнеси, които навлизат на нови пазари и привличат капитал."),
                  ("Утвърдени компании", "Развити дружества с текущи корпоративни, трудови и регулаторни нужди.")]},
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
 "bg": {"title": "За нас | SM Legal — Адвокатска кантора Марушкина",
  "desc": "Запознайте се с SM Legal — адвокатска кантора в София, фокусирана върху бизнес правото. Нашата мисия, ценности и начин на работа с български и международни клиенти.",
  "h1": "За SM Legal", "sub": "Адвокатска кантора, създадена да подкрепя бизнеса на всеки етап от неговото развитие.",
  "blocks": [
   ("Нашата мисия", ["SM Legal има за цел да подкрепя бизнеса ви изцяло и да предоставя широк спектър от отлични правни услуги, като разбира вашата дейност и цели. Подкрепяме ви в процеса на учредяване на компанията и на всеки етап от корпоративните промени и растежа.",
                     "Вярваме, че добрият адвокат не е само защитник при спор, а доверен съветник, който помага спорът изобщо да не възникне. Затова се стремим да познаваме бизнеса на клиентите си в дълбочина — техните продукти, пазари, партньори и планове."]),
   ("Кои са нашите клиенти", ["Работим с основатели на стартиращи и технологични компании, инвеститори и фондове за рисков капитал, малки и средни предприятия, чуждестранни компании, които навлизат на българския пазар, както и с физически лица — предприемачи, мениджъри и висококвалифицирани специалисти, които се установяват в България.",
                               "Обслужваме клиенти от България, държавите от Европейския съюз, Обединеното кралство, САЩ, Обединените арабски емирства и други юрисдикции, като при необходимост координираме работата с доверени партньори в чужбина."]),
   ("Как работим", ["Всяко ангажиране започва с ясно определяне на задачата, сроковете и възнаграждението. Предлагаме почасово възнаграждение, фиксирана цена за определени услуги и абонаментно правно обслужване за клиенти с постоянни нужди.",
                    "Отговаряме бързо, пишем ясно и обясняваме правните въпроси на разбираем език. Поверителността на информацията и защитата на интересите на клиента са в основата на нашата работа."])],
  "facts": [("11", "области на бизнес правото"), ("2", "езика на обслужване — BG / EN"), ("1", "работен ден — срок за отговор"), ("100%", "фокус върху бизнеса")]},
 "en": {"title": "About Us | SM Legal — Marushkina Law Firm",
  "desc": "Meet SM Legal — a Sofia law firm focused on business law. Our mission, values and way of working with Bulgarian and international clients.",
  "h1": "About SM Legal", "sub": "A law firm built to support businesses at every stage of their development.",
  "blocks": [
   ("Our mission", ["SM Legal aims to support your business entirely and to provide a wide spectrum of excellent legal services by understanding your business activity and goals. We support you in the incorporation process and during each stage of corporate change and growth.",
                    "We believe that a good lawyer is not only an advocate in a dispute but a trusted adviser who helps prevent the dispute from arising in the first place. That is why we aim to know our clients' businesses in depth — their products, markets, partners and plans."]),
   ("Who our clients are", ["We work with founders of start-ups and technology companies, investors and venture capital funds, small and medium-sized enterprises, foreign companies entering the Bulgarian market, and individuals — entrepreneurs, managers and highly qualified professionals relocating to Bulgaria.",
                            "We serve clients from Bulgaria, the European Union, the United Kingdom, the United States, the United Arab Emirates and other jurisdictions, coordinating with trusted partners abroad where needed."]),
   ("How we work", ["Every engagement starts with a clear definition of the task, timeline and fees. We offer hourly rates, fixed fees for defined services and retainer arrangements for clients with ongoing needs.",
                    "We respond quickly, write clearly and explain legal issues in plain language. Confidentiality and the protection of our clients' interests are at the heart of what we do."])],
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
    out += '<section class="stats stats--slate"><div class="wrap stats__grid">' + "".join(
        f'<div class="stat reveal"><span class="stat__n" data-count="{n}">{n}</span><span class="stat__l">{esc(l)}</span></div>' for n, l in a["facts"]) + '</div></section>'
    out += f'<section class="section section--white"><div class="wrap"><div class="sec-head"><span class="eyebrow">{"Ценности" if lang == "bg" else "Values"}</span><h2>{"Принципите, на които стъпваме" if lang == "bg" else "The principles we work by"}</h2></div><div class="values" style="grid-template-columns:repeat(2,1fr)">' + "".join(
        f'<div class="value"><h3>{esc(x)}</h3><p>{esc(y)}</p></div>' for x, y in h["values"]) + '</div></div></section>'
    out += f'<section class="section section--sand"><div class="wrap"><div class="sec-head sec-head--center"><span class="eyebrow">{h["q_eb"]}</span><h2>{h["q_h"]}</h2></div>{slider(lang)}</div></section>'
    out += clients_band(lang)
    out += cta_band(lang, path) + footer(lang, path)
    emit(path, out, lang, alt)

# ---- practice index & pages
PR_INDEX = {
 "bg": {"title": "Правни услуги за бизнеса | SM Legal — адвокат в София",
        "desc": "Правни услуги на SM Legal: търговско и корпоративно право, венчър капитал, стартъпи и IT, трудово и имиграционно право, данъци и ДДС, compliance и AML, GDPR, интелектуална собственост, имоти и спорове.",
        "h1": "Правни услуги", "sub": "Цялостно правно обслужване на бизнеса — от учредяването и инвестициите до регулаторното съответствие и защитата при спорове."},
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
 "bg": {"for": "За кого", "all": "Всички области", "services": "Какво включва", "faq": "Често задаван въпрос", "related": "Прочетете още", "more": "Цялата информация за услугата", "of": "от", "prev": "Предишна област", "next": "Следваща област", "pick": "Изберете област"},
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
            f'<div class="hub__body"><div><h3>{x["services"]}</h3><ul class="hub__list">{svc}</ul></div>'
            f'<div class="hub__side"><details class="hub__faq" open><summary>{x["faq"]}</summary><p class="hub__q">{esc(q)}</p><p>{esc(ans)}</p></details>{relh}</div></div>'
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
  "bio": ["Силвия Марушкина специализира в търговското и корпоративното право, сделките с рисков капитал и интелектуалната собственост и има дългогодишен опит в работата с български и международни клиенти.",
          "Нейната практика обхваща учредяването и корпоративното обслужване на дружества, структурирането на инвестиционни сделки, регистрацията и защитата на търговски марки в България, ЕС и по Мадридската система, както и имиграционни и трудовоправни въпроси на компании, които привличат специалисти от чужбина.",
          "Работи свободно на български и английски език и изготвя правни документи и на двата езика. Мотивацията ѝ за професионално развитие и желанието да подкрепя клиентите в постигането на целите им са довели до високо ниво на професионализъм, оценено положително от много клиенти."],
  "focus": "Основни области", "langs_h": "Езици"},
 "en": {"title": "Team — Sylvia Marushkina, Attorney-at-law | SM Legal",
  "desc": "Sylvia Marushkina, attorney-at-law — corporate and commercial law, venture capital, intellectual property, immigration and employment law. Founder of SM Legal, Sofia.",
  "h1": "Team", "sub": "Behind every solution stands a personal commitment to the client's success.",
  "bio": ["Sylvia Marushkina specialises in commercial and corporate law, venture capital transactions and intellectual property, and has long-standing experience working with Bulgarian and international clients.",
          "Her practice covers company formation and corporate housekeeping, structuring investment transactions, registering and protecting trade marks in Bulgaria, the EU and under the Madrid System, as well as immigration and employment matters for companies hiring talent from abroad.",
          "She works fluently in Bulgarian and English and drafts legal documents in both languages. Her motivation for professional growth and eagerness to help clients achieve their goals have led to a high level of professionalism, positively assessed by many clients."],
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
 <div class="portrait reveal"><img src="{rel(path, 'assets/img/Sylvia-Marushkina-3.jpg')}" alt="{t['author']}" width="800" height="1000" loading="lazy" onerror="this.remove()"></div>
 <div class="reveal"><span class="eyebrow">{a['h1']}</span><p class="role">{t['author_role']}</p><h2>{t['author']}</h2>
 {''.join('<p>'+esc(x)+'</p>' for x in a['bio'])}
 <h3 style="margin-top:30px">{a['focus']}</h3><ul class="tags">{tags}</ul>
 <p><strong>{a['langs_h']}:</strong> {t['langs']}</p>
 <div class="hero__cta"><a class="btn" href="{rel(path, ROUTES['contact'][lang])}">{t['cta']}</a><a class="btn btn--ghost" href="mailto:{EMAIL}">{EMAIL}</a></div></div>
</div></section>"""

# ---- insights
INS = {
 "bg": {"title": "Публикации — статии и новини | SM Legal",
        "desc": "Правни статии и новини от SM Legal: промени в законодателството, практически насоки за търговско право, венчър капитал, имиграция, compliance и интелектуална собственост.",
        "h1": "Публикации", "sub": "Статии, анализи и новини за законодателни промени, които засягат вашия бизнес."},
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
    out = head(lang, path, d["title"] + " | SM Legal", d["excerpt"], alt, og_type="article", schema=[bc, art])
    out += header(lang, path, "insights", alt)
    out += '<div class="read-progress" aria-hidden="true"><span></span></div>'
    out += f"""<section class="page-hero dark"><div class="wrap">{c}
<div class="post__meta" style="color:#bdb8b1"><span class="badge">{typ}</span><time datetime="{x['date']}">{fmt_date(x['date'], lang)}</time><span>{x['read']} {t['min']}</span></div>
<h1>{esc(d['title'])}</h1><p>{esc(d['excerpt'])}</p></div></section>"""
    others = [y for y in sorted_posts() if y is not x][:3]
    pr = P[x["practice"]]
    out += f"""<section class="section"><div class="wrap article-wrap">
<article class="prose">{d['body']}
<p class="disclaimer">{t['disclaimer']}</p>
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
  "desc": "Свържете се с адвокатска кантора SM Legal в София — ул. „Добротица Деспот“ 41. Заявете консултация по търговско, трудово, имиграционно право и други.",
  "h1": "Контакти", "sub": "Опишете накратко вашия въпрос и ще се свържем с вас в рамките на един работен ден.",
  "form_h": "Заявка за консултация", "name": "Име и фамилия", "email": "Имейл", "phone": "Телефон", "company": "Компания",
  "topic": "Област", "topic_any": "Изберете (по желание)", "msg": "Съобщение",
  "consent": "Съгласен/съгласна съм предоставените данни да бъдат обработвани с цел отговор на запитването ми съгласно", "send": "Изпрати",
  "ok": "Благодарим ви! Съобщението беше изпратено успешно. Ще се свържем с вас скоро.", "err": "Възникна грешка при изпращането. Моля, пишете ни на office@smlegal.bg.",
  "map": "Вижте на картата"},
 "en": {"title": "Contact — Request a Consultation | SM Legal, Sofia",
  "desc": "Contact SM Legal law firm in Sofia, Bulgaria — 41 Dobrotitsa Despot Str. Request a consultation on corporate, employment, immigration law and more.",
  "h1": "Contact", "sub": "Briefly describe your question and we will get back to you within one business day.",
  "form_h": "Consultation request", "name": "Full name", "email": "Email", "phone": "Phone", "company": "Company",
  "topic": "Practice area", "topic_any": "Select (optional)", "msg": "Message",
  "consent": "I agree that the data provided will be processed for the purpose of responding to my enquiry in accordance with the", "send": "Send",
  "ok": "Thank you! Your message has been sent successfully. We will be in touch soon.", "err": "Something went wrong. Please email us at office@smlegal.bg.",
  "map": "View on map"},
}
def build_contact(lang):
    a = CONTACT[lang]; t = T[lang]
    path = ROUTES["contact"][lang]; alt = ROUTES["contact"]["en" if lang == "bg" else "bg"]
    hero, bc = page_hero(lang, path, [(a["h1"], path)], a["h1"], a["sub"])
    out = head(lang, path, a["title"], a["desc"], alt, schema=[bc, {"@type": "ContactPage", "url": url(path), "about": {"@id": ORG_ID}}])
    out += header(lang, path, "contact", alt) + hero
    opts = "".join(f'<option>{esc(p[lang]["title"])}</option>' for p in PRACTICES)
    maps = "https://www.google.com/maps/search/?api=1&query=" + "Dobrotitsa+Despot+41,+Sofia+1612"
    out += f"""<section class="section"><div class="wrap contact-grid">
<div class="reveal">
 <ul class="info-list">
  <li>{icon('pin')}<div><strong>{t['address_l']}</strong>{t['address']}<br><a class="link-arrow" href="{maps}" target="_blank" rel="noopener">{a['map']}</a></div></li>
  <li>{icon('mail')}<div><strong>{t['email_l']}</strong><a href="mailto:{EMAIL}">{EMAIL}</a></div></li>
  <li>{icon('clock')}<div><strong>{t['hours_l']}</strong>{t['hours']}</div></li>
  <li>{icon('chat')}<div><strong>{t['langs_l']}</strong>{t['langs']}</div></li>
 </ul>
</div>
<form class="form reveal" action="{rel(path, 'contact.php')}" method="post">
 <h2 style="font-size:2rem">{a['form_h']}</h2>
 <p class="form-note" data-form-status data-ok="{esc(a['ok'])}" data-err="{esc(a['err'])}" hidden role="status"></p>
 <input type="hidden" name="lang" value="{lang}">
 <div class="hp" aria-hidden="true"><label>Website<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
 <div class="row"><div class="field"><label for="f-name">{a['name']} *</label><input id="f-name" name="name" required autocomplete="name"></div>
 <div class="field"><label for="f-company">{a['company']}</label><input id="f-company" name="company" autocomplete="organization"></div></div>
 <div class="row"><div class="field"><label for="f-email">{a['email']} *</label><input id="f-email" type="email" name="email" required autocomplete="email"></div>
 <div class="field"><label for="f-phone">{a['phone']}</label><input id="f-phone" type="tel" name="phone" autocomplete="tel"></div></div>
 <div class="field"><label for="f-topic">{a['topic']}</label><select id="f-topic" name="topic"><option value="">{a['topic_any']}</option>{opts}</select></div>
 <div class="field"><label for="f-msg">{a['msg']} *</label><textarea id="f-msg" name="message" required></textarea></div>
 <label class="check"><input type="checkbox" name="consent" value="1" required><span>{a['consent']} <a href="{rel(path, ROUTES['privacy'][lang])}">{t['privacy'].lower()}</a>.</span></label>
 <button class="btn" type="submit">{a['send']}</button>
</form>
</div></section>"""
    out += footer(lang, path)
    emit(path, out, lang, alt)

# ---- privacy
PRIV = {
 "bg": {"title": "Политика за поверителност | SM Legal", "h1": "Политика за поверителност",
  "desc": "Политика за поверителност на SM Legal — как обработваме личните данни, предоставени чрез уебсайта smlegal.bg.",
  "body": """<p>Настоящата политика описва как SM Legal — Адвокатска кантора Марушкина („ние“) обработва личните данни на посетителите на уебсайта smlegal.bg и на лицата, които се свързват с нас.</p>
<h2>Администратор на данните</h2><p>Адвокат Силвия Марушкина, адрес: гр. София 1612, ул. „Добротица Деспот“ 41, имейл: office@smlegal.bg.</p>
<h2>Какви данни обработваме</h2><p>Обработваме данните, които ни предоставяте чрез формата за контакт или по имейл — име, имейл адрес, телефон, наименование на компанията и съдържанието на съобщението ви.</p>
<h2>Цели и правно основание</h2><ul><li>отговор на вашето запитване и предприемане на стъпки преди сключване на договор за правна помощ — чл. 6, пар. 1, б. „б“ от Регламент (ЕС) 2016/679 (GDPR);</li><li>изпълнение на законови задължения, включително по Закона за адвокатурата и Закона за мерките срещу изпирането на пари — чл. 6, пар. 1, б. „в“ от GDPR;</li><li>съгласие, предоставено чрез формата за контакт — чл. 6, пар. 1, б. „а“ от GDPR.</li></ul>
<h2>Срок на съхранение</h2><p>Данните от запитвания, които не са довели до ангажиране, се съхраняват до 12 месеца. Данните на клиенти се съхраняват за сроковете, предвидени в приложимото законодателство.</p>
<h2>Получатели</h2><p>Не предоставяме данните ви на трети лица, освен на доставчици на хостинг и имейл услуги, които действат по наше възлагане, или когато това се изисква по закон. Адвокатската тайна се спазва по всяко време.</p>
<h2>Бисквитки</h2><p>Уебсайтът не използва рекламни или аналитични бисквитки. Шрифтовете се зареждат от услугата Google Fonts.</p>
<h2>Вашите права</h2><p>Имате право на достъп, коригиране, изтриване, ограничаване на обработването, преносимост и възражение, както и право да оттеглите съгласието си по всяко време. Можете да упражните правата си, като ни пишете на office@smlegal.bg. Имате право да подадете жалба до Комисията за защита на личните данни (www.cpdp.bg).</p>
<p><em>Последна актуализация: октомври 2026 г.</em></p>"""},
 "en": {"title": "Privacy Policy | SM Legal", "h1": "Privacy Policy",
  "desc": "SM Legal privacy policy — how we process personal data submitted through the smlegal.bg website.",
  "body": """<p>This policy explains how SM Legal — Marushkina Law Firm ("we") processes the personal data of visitors to smlegal.bg and of persons who contact us.</p>
<h2>Data controller</h2><p>Attorney-at-law Sylvia Marushkina, 41 Dobrotitsa Despot Str., Sofia 1612, Bulgaria, email: office@smlegal.bg.</p>
<h2>Data we process</h2><p>We process the data you provide via the contact form or by email — name, email address, phone number, company name and the content of your message.</p>
<h2>Purposes and legal basis</h2><ul><li>responding to your enquiry and taking steps prior to entering into an engagement — Art. 6(1)(b) of Regulation (EU) 2016/679 (GDPR);</li><li>compliance with legal obligations, including under the Bar Act and anti-money laundering legislation — Art. 6(1)(c) GDPR;</li><li>consent given through the contact form — Art. 6(1)(a) GDPR.</li></ul>
<h2>Retention</h2><p>Data from enquiries that do not result in an engagement are kept for up to 12 months. Client data are kept for the periods required by applicable law.</p>
<h2>Recipients</h2><p>We do not disclose your data to third parties, except to hosting and email service providers acting on our behalf, or where required by law. Attorney–client privilege is observed at all times.</p>
<h2>Cookies</h2><p>This website does not use advertising or analytics cookies. Fonts are loaded from the Google Fonts service.</p>
<h2>Your rights</h2><p>You have the right of access, rectification, erasure, restriction of processing, data portability and objection, and the right to withdraw consent at any time. You may exercise your rights by writing to office@smlegal.bg. You also have the right to lodge a complaint with the Commission for Personal Data Protection (www.cpdp.bg).</p>
<p><em>Last updated: October 2026</em></p>"""},
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
<h1>Страницата не е намерена</h1><p>Page not found. The page you are looking for may have been moved.</p>
<div class="hero__cta" style="margin-top:30px"><a class="btn" href="/">Начало</a><a class="btn btn--ghost" href="/en/">Home (EN)</a></div></div></section>"""
    out += footer("bg", path)
    out = out.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<base href="/">', 1)
    emit(path, out, sitemap=False)

# ---------------------------------------------------------------- write
def write_all():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"), OUT)
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
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /contact.php\n\nSitemap: {SITE}/sitemap.xml\n")
    print(len(PAGES), "pages")

if __name__ == "__main__":
    write_all()
