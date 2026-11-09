# Nivalis design kit

Cold-storage building operations (IoT/BMS). Calm, light, operator-first. Petrol and aqua surfaces, one coral signal, flat buttons, hairline rows, lots of air.
Product: Nivalis Building Operations. Facility BCD-01, Baltimore Cold Distribution Center. Organization: Harlow Cold Logistics.

## What is inside
- tokens.css: colors, type, radii
- logo/: Nivalis lockup (mark and wordmark)
- reference-screens/desktop: 10 approved screens, 2560x1600 (Conditions, Incident, Equipment EF-3, Energy, Inventory hold, Remote action in 5 states)
- reference-screens/mobile: 12 approved screens, 1179x2556 (Conditions x3 are the first, older pass; Incident, EF-3, Energy, Hold, Remote action x5 follow the current rules)
- preview/nivalis-kit-overview.png: one-page board of tokens and components
- src/: Python plus Playwright generators (common.py holds data and charts, mobile2.py and mobile3.py hold mobile components)
- skill/SKILL.md: the working rules for Claude

## Rebuild
1. npm install @fontsource/onest @fontsource/bricolage-grotesque (path is set in src/common.py as FONTS)
2. pip install playwright, use system Chrome or playwright chromium
3. python3 src/incident.py, equip.py, hold.py, energy.py, action.py (desktop, 1600x1000 at 1.6)
4. python3 src/mobile2.py, mobile3.py (mobile, 393x852 at 3)

## Rules of the system
- Fonts: Bricolage Grotesque 500 to 700 for titles and key numbers, Onest 400 to 600 for UI. Not Inter.
- Main pages (Conditions, Energy) carry the dark petrol hero. Secondary pages (Incident, Equipment, Hold, Remote action) carry the light aqua hero. Never a hero on every page.
- Approval is a flat green record with a check circle, not an info block. An active process (queued, running) lives in its own aqua container, apart from accordions.
- Floating action bar sits on top, content continues under it. On mobile it is a blurred bar with a hairline top, primary 50 pt.
- Tags only for exceptions. No pill next to every number.
- Charts: one line, a dashed limit or normal, one red zone, an end label. No gridlines, axes or legends when direct labels fit. Charts fill the free space instead of leaving gaps.
- Mobile: one dominant element, plain rows on the page background, extra content goes below the fold. Sheets for modals, never centered dialogs.
- No middle dots, bullets or long dashes in text. Use columns, spacing or commas.
- Story clock: Fri, Nov 6, 10:24 EST. Approval 10:25, queued 10:26.
- Shared facts: zone -16.1 C, limit -18.0 C, deviation +1.9 C, EF-3 4.5 A (normal 4.8 A), CR-01 26.9 kW (normal 32.4 kW), demand 48.2 kW, projected 51.7 kW, capacity 66.8 kW, incident EXC-2417 opened 04:24, hold HOLD-2417 with 42 pallets in 4 lots, action ACT-1184 on CTRL-FZB-03, policy POL-COLD-07.
- People on the current story: Felix Whitaker (owner and approver), Rafael Ibarra (FSQA reviewer), Luis Ortega (control-room operator). New projects get new names.
