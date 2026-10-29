# Cyberguard design kit

Light, refined, Ramp-like UI for the Cyberguard cybersecurity product.
Burgundy primary, one accent only, flat buttons, hairline rows, lots of air.

## What is inside
- tokens.css: colors (burgundy primary #6B1D4A, orange for high risk, green and amber only for status)
- logo/: Cyberguard logo cut out in ink color (full and mark)
- assets/: avatars used in screens (Katerina, Maya Chen, Jordan Diaz, Daniel Okafor)
- reference-screens/: the 8 approved screens, 2560x1664
- build_cyberguard.py: renders all 8 screens (HTML plus Chromium, 1600x1040 at 1.6)

## Rebuild
1. npm install
2. pip install playwright, then playwright install chromium
3. python build_cyberguard.py  (PNG and HTML land in out/)

## Rules of the system
- Font Hanken Grotesk, thin weights (400 to 520), titles with negative tracking
- Sidebar 236px, top bar 60px, right rail 372 to 392px; Security group expands with Overview, Incidents, Exposures, Identities
- Approvals badge is 3 everywhere; story time "now" is Oct 26, 2026, 02:42 UTC
- Incident INC-2026-0837 Sensitive data exfiltration attempt, owner Daniel Okafor, approver Jordan Diaz, user Maya Chen
- No dots in badges, no middle dots in text (use commas), no gradients on buttons
- Right panels: fixed header, scroll area with fade and thin scrollbar thumb, pinned footer actions
- Charts: thin lines or bars, soft tinted area, step lines for discrete events, annotated markers, end labels, no legends when direct labels fit
- Every new class gets a unique prefix (x, y, z, q, k, v) because base class names collide
