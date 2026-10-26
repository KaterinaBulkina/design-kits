#!/usr/bin/env python3
"""Shared HTML -> PNG renderer for every kit in design-kits.

Niche-agnostic. What it does:
  1. reads a kit template (*.src.html);
  2. replaces __FONTS__ with the local fontsource folder (shared/fonts/node_modules);
  3. replaces __MARK__ / __WORD__ with the kit's logo PNG masks (base64);
  4. resolves photos/avatars/screen.png from --assets (per-project folder, not in the repo);
  5. renders each state with Playwright and optionally runs a kit check script.

Example (healthcare screen, both states):
  python3 shared/render/render.py \
    --template healthcare/templates/screen-glass-template.src.html \
    --logo-dir healthcare/logo --assets ~/project/assets \
    --size 1600x1000 --scale 1.6 --states main=,fail=#fail \
    --check healthcare/templates/checks/screen-check.js \
    --out-dir ~/project/out --name screen
"""
import argparse, base64, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]          # design-kits/
FONTS = ROOT / "shared" / "fonts" / "node_modules"
LOGO_KEYS = {"__MARK__": "{brand}-mark.png", "__WORD__": "{brand}-word.png"}


def b64(path):
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()


def build(args):
    src = pathlib.Path(args.template).resolve()
    html = src.read_text(encoding="utf-8")
    if "__FONTS__" in html:
        if not FONTS.is_dir():
            sys.exit(f"Fonts missing: run `npm install` in {FONTS.parent}")
        html = html.replace("__FONTS__", FONTS.as_uri())
    logo_dir = pathlib.Path(args.logo_dir).resolve()
    for key, pattern in LOGO_KEYS.items():
        if key in html:
            html = html.replace(key, b64(logo_dir / pattern.format(brand=args.brand)))
    assets = pathlib.Path(args.assets).resolve() if args.assets else src.parent
    html = html.replace("<head>", f'<head><base href="{assets.as_uri()}/">', 1)
    out_dir = pathlib.Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    built = out_dir / f".{args.name}.build.html"
    built.write_text(html, encoding="utf-8")
    return built, out_dir


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--template", required=True)
    p.add_argument("--logo-dir", required=True, help="kit logo folder with <brand>-mark.png / <brand>-word.png")
    p.add_argument("--brand", default="elyra", help="logo file prefix")
    p.add_argument("--assets", help="folder with photos, avatars, screen.png (defaults to template folder)")
    p.add_argument("--size", default="1600x1000", help="CSS viewport WxH")
    p.add_argument("--scale", type=float, default=1.6, help="device scale factor")
    p.add_argument("--states", default="main=", help="name=#hash pairs, comma-separated")
    p.add_argument("--check", help="JS file evaluated on the first state; result printed as JSON")
    p.add_argument("--wait", type=int, default=800, help="ms to wait before screenshot")
    p.add_argument("--out-dir", default="out")
    p.add_argument("--name", default="render")
    args = p.parse_args()

    w, h = (int(x) for x in args.size.lower().split("x"))
    built, out_dir = build(args)
    check_js = pathlib.Path(args.check).read_text() if args.check else None

    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=args.scale)
        for i, pair in enumerate(s for s in args.states.split(",") if s):
            state, _, hsh = pair.partition("=")
            pg.goto(built.as_uri() + hsh); pg.reload(); pg.wait_for_timeout(args.wait)
            if check_js and i == 0:
                print(json.dumps(pg.evaluate(check_js), ensure_ascii=False))
            out = out_dir / f"{args.name}-{state}.png"
            pg.screenshot(path=str(out)); print(out)
        b.close()
    built.unlink()


if __name__ == "__main__":
    main()
