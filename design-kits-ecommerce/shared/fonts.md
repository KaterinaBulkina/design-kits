# Шрифты

Все шрифты локальные, из [fontsource](https://fontsource.org) (вариативные версии). Ставятся одной командой:

```bash
cd shared/fonts && npm install
```

Файлы появляются в `shared/fonts/node_modules/@fontsource-variable/<font>/files/`. В шаблонах путь к ним записан как `__FONTS__/@fontsource-variable/...`; `shared/render/render.py` подставляет реальный путь сам. `node_modules` в репозиторий не коммитится.

| Шрифт | Пакет | Роль | Киты |
|---|---|---|---|
| Space Grotesk | `@fontsource-variable/space-grotesk` | заголовки, большие цифры, заголовки панелей (500, letter-spacing −0.025em) | healthcare |
| Plus Jakarta Sans | `@fontsource-variable/plus-jakarta-sans` | весь UI-текст | healthcare |
| Geist Mono | `@fontsource-variable/geist-mono` | ID, таймстемпы | healthcare |
| Schibsted Grotesk | `@fontsource-variable/schibsted-grotesk` | весь текст интернет-магазина (400-650), заголовки и цены | ecommerce |

Новый шрифт для кита: добавить пакет в `shared/fonts/package.json` и строку в эту таблицу.

## Запрещено

- **Instrument Serif** и любые высокие узкие (condensed) антиквы такого типа — нигде: заголовки, цифры, спецификации, бенто.
- Inter, Roboto, Arial и системные шрифты как основной шрифт.

Идеи для новых пар шрифтов: [typ.io/samples](https://typ.io/samples).
