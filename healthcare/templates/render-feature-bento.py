#!/usr/bin/env python3
"""Elyra feature bento -> PNG. Thin wrapper over shared/render/render.py (see that file for options).
Usage: python3 healthcare/templates/render-feature-bento.py --assets <project assets dir> --out-dir <out dir>
Extra flags are passed through (e.g. --template to point at an edited copy)."""
import pathlib, subprocess, sys
KIT = pathlib.Path(__file__).resolve().parents[1]
RENDER = KIT.parent / "shared" / "render" / "render.py"
args = ["--template", str(KIT / "templates" / "feature-bento-template.src.html"), "--logo-dir", str(KIT / "logo"), "--brand", "elyra",
        "--size", "1440x936", "--scale", str(2560 / 1440), "--wait", "800", "--name", "feature-bento"]
sys.exit(subprocess.call([sys.executable, str(RENDER), *args, *sys.argv[1:]]))
