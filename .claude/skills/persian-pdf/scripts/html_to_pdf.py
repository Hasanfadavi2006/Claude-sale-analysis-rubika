#!/usr/bin/env python3
"""Render an HTML file to PDF (or PNG) using headless Chromium.

Usage:
    python3 html_to_pdf.py input.html output.pdf
    python3 html_to_pdf.py input.html /tmp/preview.png --screenshot

Auto-locates a Chromium/Chrome binary. Designed for Persian/RTL documents whose
fonts are embedded as base64 in the HTML, so no network is needed at render time.
"""
import os
import sys
import shutil
import subprocess

# Common locations, in priority order. Playwright's bundled Chromium first.
CANDIDATES = [
    "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
]
PATH_NAMES = ["chromium", "chromium-browser", "google-chrome",
              "google-chrome-stable", "chrome"]


def find_chromium():
    # explicit candidates
    for c in CANDIDATES:
        if os.path.isfile(c) and os.access(c, os.X_OK):
            return c
    # any chromium under /opt/pw-browsers
    pw = "/opt/pw-browsers"
    if os.path.isdir(pw):
        for root, _dirs, files in os.walk(pw):
            if "chrome" in files:
                p = os.path.join(root, "chrome")
                if os.access(p, os.X_OK):
                    return p
    # PATH
    for name in PATH_NAMES:
        p = shutil.which(name)
        if p:
            return p
    return None


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    inp = os.path.abspath(sys.argv[1])
    out = os.path.abspath(sys.argv[2])
    screenshot = "--screenshot" in sys.argv[3:]

    if not os.path.isfile(inp):
        print(f"ERROR: input not found: {inp}")
        sys.exit(1)

    chrome = find_chromium()
    if not chrome:
        print("ERROR: no Chromium/Chrome found. Try:\n"
              "  npx puppeteer browsers install chrome")
        sys.exit(1)

    url = "file://" + inp
    base = ["--headless", "--no-sandbox", "--disable-gpu",
            "--disable-dev-shm-usage", "--hide-scrollbars",
            "--font-render-hinting=none"]

    if screenshot:
        cmd = [chrome] + base + [
            "--force-device-scale-factor=2",
            "--window-size=820,1160",
            f"--screenshot={out}", url,
        ]
    else:
        cmd = [chrome] + base + [
            "--no-pdf-header-footer",
            f"--print-to-pdf={out}", url,
        ]

    r = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    if not os.path.isfile(out) or os.path.getsize(out) == 0:
        sys.stderr.write(r.stderr.decode("utf-8", "ignore"))
        print(f"ERROR: render produced no output ({out})")
        sys.exit(1)
    kind = "PNG" if screenshot else "PDF"
    print(f"{kind} written: {out}  ({os.path.getsize(out)} bytes)  via {chrome}")


if __name__ == "__main__":
    main()
