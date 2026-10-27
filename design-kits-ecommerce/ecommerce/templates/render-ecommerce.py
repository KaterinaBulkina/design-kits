#!/usr/bin/env python3
"""Ecommerce kit: cart (+edit-kit modal), product page (+mini cart), checkout -> PNG 2560x1664.
Thin wrapper over shared/render/render.py.
Usage: python3 ecommerce/templates/render-ecommerce.py --assets <folder with photos + av.jpg> --out-dir <out>
Without --assets the sample Ember photos from ecommerce/sample-assets are used (avatar av.jpg must be added: put your own photo there).
Extra flags are passed through; --only cart|pdp|checkout renders one screen."""
import pathlib, subprocess, sys
KIT = pathlib.Path(__file__).resolve().parents[1]
RENDER = KIT.parent / "shared" / "render" / "render.py"
argv = sys.argv[1:]
only = None
if "--only" in argv:
    i = argv.index("--only"); only = argv[i + 1]; del argv[i:i + 2]
if "--assets" not in argv:
    argv += ["--assets", str(KIT / "sample-assets")]
JOBS = [("cart", "cart-template.src.html", "main=,modal=#modal"),
        ("pdp", "pdp-template.src.html", "main=,minicart=#cart"),
        ("checkout", "checkout-template.src.html", "main=")]
rc = 0
for name, tpl, states in JOBS:
    if only and only != name: continue
    rc |= subprocess.call([sys.executable, str(RENDER), "--template", str(KIT / "templates" / tpl), "--logo-dir", str(KIT / "logo"),
        "--brand", "ember", "--size", "1280x832", "--scale", "2", "--states", states, "--wait", "700",
        "--check", str(KIT / "templates" / "checks" / "screen-check.js"), "--name", name, *argv])
sys.exit(rc)
