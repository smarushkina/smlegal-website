# SM Legal — smlegal.bg

Двуезичен (BG / EN) уебсайт на SM Legal — Адвокатска кантора Марушкина, София.

## Структура
- Коренът на хранилището е готовият сайт — публикува се чрез GitHub Pages (клон `main`, папка `/`) на домейна smlegal.bg (файл `CNAME`).
- `index.html` и останалите `.html` в корена — българска версия; `en/` — английска версия.
- `pravni-uslugi/`, `en/practice-areas/` — 11 страници за правни услуги.
- `publikatsii/`, `en/insights/` — статии и новини.
- `assets/` — стилове, скриптове, лого (`assets/img/brand/`), иконки.
- Контакти: бутон за имейл (mailto) вместо форма — GitHub Pages не изпълнява PHP.
- Бисквитки: банер за съгласие (`assets/js/main.js`); Google Analytics се зарежда само след изрично съгласие и само ако в `_source/build.py` е зададен `GA_ID` (в HTML: атрибут `data-ga` на `#cookie`).
- Шрифтовете са в `assets/fonts/` (без заявки към Google Fonts).
- `CNAME`, `.nojekyll`, `robots.txt`, `sitemap.xml`, `404.html` — файлове за GitHub Pages и SEO. `ekip.html` и `en/team.html` пренасочват към „За нас“.
- `_source/` — генератор на сайта (Python): `python3 build.py --publish` сглобява сайта и го копира в корена.
  Всички текстове и промени по страниците са пренесени в `content_*.py` / `build.py` — генераторът създава сайта точно във вида, в който е публикуван. При бъдещи промени редактирайте източниците в `_source/` и стартирайте `python3 build.py --publish`.

## Преди публикуване
1. Добавете снимката `assets/img/Sylvia-Marushkina-3.jpg` и логата на партньорите от стария сайт в `assets/img/`.
2. Подайте `https://smlegal.bg/sitemap.xml` в Google Search Console.
