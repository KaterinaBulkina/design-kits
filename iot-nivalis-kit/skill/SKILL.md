---
name: nivalis-design-system
description: Use when designing or extending Nivalis Building Operations (cold-storage IoT/BMS) screens, desktop or mobile. Gives tokens, page types, components, chart and copy rules, and the shared story data.
---
# Nivalis design system

Start from the kit: clone github.com/KaterinaBulkina/design-kits, folder nivalis-kit. Read README.md and tokens.css, then open 2 to 3 closest screens in reference-screens before drawing anything.

## Page types
- Main page (Conditions, Energy): dark petrol hero, one key figure, tabs under the header on mobile.
- Secondary page (Incident, Equipment, Inventory hold, Remote action): back button, centered title, light aqua hero with the key figure and a short facts grid, then content on the page background.
- Modal flows: desktop centered modal, mobile bottom sheet with grabber, summary rows, one checkbox, Cancel and primary.

## Components
- Approval record: flat green block, check circle, who and when, then locked parameters. Never the aqua info style.
- Active process (queued, running): separate aqua container with a vertical timeline, apart from accordions.
- Rows: plain on the page, hairline separators, tag only on exceptions.
- Action bar: floating on desktop, blurred bar on mobile, one primary and one secondary.

## Charts
One line, a dashed limit, one red zone, an end label. Fill the free space. No gridlines or legends when labels fit. Take real chart shapes from chart-references.

## Copy
Short phrases an operator reads at a glance. No middle dots or long dashes. Cut paragraphs. Every person gets a new first and last name per project.

## Story data
Keep numbers consistent: Fri Nov 6 10:24 EST, zone B -16.1 C vs limit -18.0 C, EXC-2417 since 04:24, EF-3 4.5 A vs 4.8 A, CR-01 26.9 kW vs 32.4 kW, demand 48.2 to 51.7 kW with 66.8 kW capacity, HOLD-2417 42 pallets, ACT-1184 CTRL-FZB-03 POL-COLD-07.

## Mobile export
Separate PNGs 1179x2556 from a 393x852 element at 3x, no background or device frame, safe areas 59 top and 34 bottom, type 15 and up except captions at 12.5.
