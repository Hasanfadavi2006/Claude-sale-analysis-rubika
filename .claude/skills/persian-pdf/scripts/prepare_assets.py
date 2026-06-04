#!/usr/bin/env python3
"""Ensure the Vazirmatn Persian font is available and emit its base64.

- Downloads Vazirmatn Regular + Bold TTFs to /tmp if missing (GitHub raw, which
  is reachable in this environment; the jsdelivr CDN is usually blocked).
- Writes base64 to /tmp/vazir_reg_b64.txt and /tmp/vazir_bold_b64.txt.
- Validates the files are real TrueType (guards against an HTML error page being
  saved as a .ttf).

Run with the Bash tool using dangerouslyDisableSandbox: true (network needed).
"""
import base64
import os
import sys
import urllib.request

VER = "v33.003"
BASE = f"https://raw.githubusercontent.com/rastikerdar/vazirmatn/{VER}/fonts/ttf"
FONTS = {
    "Regular": "/tmp/Vazirmatn-Regular.ttf",
    "Bold": "/tmp/Vazirmatn-Bold.ttf",
}
B64 = {
    "Regular": "/tmp/vazir_reg_b64.txt",
    "Bold": "/tmp/vazir_bold_b64.txt",
}


def valid_ttf(path):
    if not os.path.isfile(path) or os.path.getsize(path) < 50000:
        return False
    with open(path, "rb") as f:
        sig = f.read(4)
    # 0x00010000 (TrueType) or 'OTTO' or 'true'
    return sig in (b"\x00\x01\x00\x00", b"OTTO", b"true", b"ttcf")


def main():
    for weight, path in FONTS.items():
        if not valid_ttf(path):
            url = f"{BASE}/Vazirmatn-{weight}.ttf"
            print(f"downloading {weight} from {url}")
            try:
                urllib.request.urlretrieve(url, path)
            except Exception as e:  # noqa
                print(f"ERROR downloading {weight}: {e}")
                sys.exit(1)
        if not valid_ttf(path):
            print(f"ERROR: {path} is not a valid TTF after download "
                  f"(size={os.path.getsize(path) if os.path.isfile(path) else 0})")
            sys.exit(1)
        b64 = base64.b64encode(open(path, "rb").read()).decode()
        open(B64[weight], "w").write(b64)
        print(f"{weight}: ok  ({os.path.getsize(path)} bytes, "
              f"b64 -> {B64[weight]})")
    print("\nDone. Paste the base64 from those files into the @font-face src "
          "of your HTML template.")


if __name__ == "__main__":
    main()
