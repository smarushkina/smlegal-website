# SM Legal — smlegal.bg

Двуезичен (BG / EN) уебсайт на SM Legal — Адвокатска кантора Марушкина, София.

## Структура
- Коренът на хранилището е готовият сайт — качва се директно в `public_html` на хостинга.
- `index.html` и останалите `.html` в корена — българска версия; `en/` — английска версия.
- `pravni-uslugi/`, `en/practice-areas/` — 11 страници за правни услуги.
- `publikatsii/`, `en/insights/` — статии и новини.
- `assets/` — стилове, скриптове, лого (`assets/img/brand/`), иконки.
- `contact.php` — обработка на формата за контакт (изисква PHP `mail()`).
- `.htaccess`, `robots.txt`, `sitemap.xml`, `404.html` — сървърни и SEO файлове.
- `_source/` — генератор на сайта (Python): текстовете са в `content_*.py`, шаблоните — в `build.py`.

## Преди публикуване
1. Добавете снимката `assets/img/Sylvia-Marushkina-3.jpg` и логата на партньорите от стария сайт в `assets/img/`.
2. Подайте `https://smlegal.bg/sitemap.xml` в Google Search Console.
