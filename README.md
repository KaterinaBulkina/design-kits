# design-kits

Дизайн-киты по нишам. Каждый кит — готовая утверждённая система (логотип, токены, шаблоны экрана и бенто), от которой продолжают новые проекты этой ниши, а не начинают с нуля. Файлы отсюда клонирует скилл `ui-screen-from-brief`.

| Ниша | Система | Папка | Логотип | Основные цвета | Шрифты |
|---|---|---|---|---|---|
| Healthcare | Elyra | [`healthcare/`](healthcare/) | [`healthcare/logo/`](healthcare/logo/) | forest `#123A31`, sage `#D3E3DC`, cream `#F6EFDF`, gold `#D9A441`, ink `#0F1F1A` | Space Grotesk, Plus Jakarta Sans, Geist Mono |

## Структура

```
design-kits/
  README.md          эта таблица
  shared/
    render/          общий рендер HTML → PNG (не зависит от ниши)
    fonts/           package.json со шрифтами fontsource (npm install)
    fonts.md         список шрифтов и запреты
  <niche>/           один кит = одна папка
    README.md        правила кита
    logo/            SVG, PNG-маски, оригинал
    tokens.css
    templates/       шаблоны *.src.html, обёртки рендера, checks/
    preview/         превью PNG
```

## Быстрый старт

```bash
git clone https://github.com/KaterinaBulkina/design-kits
cd design-kits/shared/fonts && npm install && cd ../..
pip install playwright && playwright install chromium
python3 healthcare/templates/render-screen.py --assets <папка с фото и аватарами> --out-dir out
```

## Как добавить новый кит

1. Скопировать папку `healthcare/` в `<ниша>/` (например `fintech/`).
2. Заменить логотип в `logo/`: SVG, PNG-маски `<brand>-mark.png` и `<brand>-word.png`, оригинал.
3. Поменять `tokens.css` и цвета/шрифты в шаблонах `templates/*.src.html`.
4. В обёртках `templates/render-*.py` поменять `--brand` на префикс нового логотипа; под новые шаблоны поправить `templates/checks/*.js`.
5. Новые шрифты — в `shared/fonts/package.json` и `shared/fonts.md`.
6. Переписать `<ниша>/README.md` и положить превью в `preview/`.
7. Добавить строку в таблицу выше.

`shared/` при этом не трогается: рендер общий для всех китов.
