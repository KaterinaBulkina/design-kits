#!/usr/bin/env python3
"""Elyra screen (main + critical state) -> PNG. Thin wrapper over shared/render/render.py (see that file for options).
Usage: python3 healthcare/templates/render-screen.py --assets <project assets dir> --out-dir <out dir>
Extra flags are passed through (e.g. --template to point at an edited copy)."""
import pathlib, subprocess, sys
KIT = pathlib.Path(__file__).resolve().parents[1]
RENDER = KIT.parent / "shared" / "render" / "render.py"
args = ["--template", str(KIT / "templates" / "screen-glass-template.src.html"), "--logo-dir", str(KIT / "logo"), "--brand", "elyra",
        "--size", "1600x1000", "--scale", "1.6", "--states", "main=,fail=#fail", "--wait", "700",
        "--check", str(KIT / "templates" / "checks" / "screen-check.js"), "--name", "screen"]
sys.exit(subprocess.call([sys.executable, str(RENDER), *args, *sys.argv[1:]]))
