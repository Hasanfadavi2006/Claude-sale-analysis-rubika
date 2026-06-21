#!/usr/bin/env python3
"""Ensure the Vazirmatn Persian font is available and emit its base64.

- Downloads Vazirmatn Regular + Bold TTFs to a temp dir if missing (GitHub raw,
  which is reachable in most environments; the jsdelivr CDN is usually blocked).
- Writes base64 next to the TTFs (vazir_reg_b64.txt / vazir_bold_b64.txt).
- Validates the files are real TrueType (guards against an HTML error page being
  saved as a .ttf).

Cross-platform: the output directory is the system temp dir (Linux: /tmp,
Windows: %TEMP%). TLS verification uses certifi's CA bundle when available so
the download works on machines whose default trust store can't verify GitHub
(common on Windows).

Run with network access available.
"""
import base64
import os
import ssl
import sys
import tempfile
import urllib.request

VER = "v33.003"
BASE = f"https://raw.githubusercontent.com/rastikerdar/vazirmatn/{VER}/fonts/ttf"
TMP = tempfile.gettempdir()
FONTS = {
    "Regular": os.path.join(TMP, "Vazirmatn-Regular.ttf"),
    "Bold": os.path.join(TMP, "Vazirmatn-Bold.ttf"),
}
B64 = {
    "Regular": os.path.join(TMP, "vazir_reg_b64.txt"),
    "Bold": os.path.join(TMP, "vazir_bold_b64.txt"),
}


def make_ssl_context():
    """Prefer certifi's CA bundle; fall back to the system default."""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:  # noqa
        return ssl.create_default_context()


def download(url, path, ctx):
    with urllib.request.urlopen(url, context=ctx) as resp:
        data = resp.read()
    with open(path, "wb") as f:
        f.write(data)


def valid_ttf(path):
    if not os.path.isfile(path) or os.path.getsize(path) < 50000:
        return False
    with open(path, "rb") as f:
        sig = f.read(4)
    # 0x00010000 (TrueType) or 'OTTO' or 'true'
    return sig in (b"\x00\x01\x00\x00", b"OTTO", b"true", b"ttcf")


def main():
    ctx = make_ssl_context()
    for weight, path in FONTS.items():
        if not valid_ttf(path):
            url = f"{BASE}/Vazirmatn-{weight}.ttf"
            print(f"downloading {weight} from {url}")
            try:
                download(url, path, ctx)
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
