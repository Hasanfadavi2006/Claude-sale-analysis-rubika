---
name: persian-pdf
description: Generate polished, print-ready PDFs from RTL/Persian (or any) HTML using a headless Chromium engine with a self-embedded Vazirmatn font. Use whenever the user wants a PDF document — receipts (رسید), official forms, invoices (فاکتور), reports (گزارش), confirmations (تأییدیه), certificates, or any styled Persian/Farsi/Arabic A4 document. Produces correct RTL shaping, embedded fonts (renders identically everywhere), embedded images, and exact-color backgrounds.
---

# Persian / RTL PDF Generator

This skill captures the reliable method for turning hand-written HTML/CSS into a
clean, print-ready PDF — with correct Persian (RTL) text shaping, embedded fonts,
embedded images, and full background/color fidelity.

## Why this method

Most "HTML → PDF" routes fail on Persian: missing fonts render boxes (□□□), web
CDNs for fonts are often blocked, and many converters drop background colors.
This method avoids all of that:

- **Headless Chromium** does the rendering → perfect RTL shaping, flexbox/grid,
  gradients, `@page` sizing. Same engine as Chrome, so WYSIWYG.
- **Vazirmatn font embedded as base64** directly in the HTML `@font-face` → the
  PDF looks identical on every machine and no network font fetch is needed at
  print time.
- `--print-to-pdf` with `--no-pdf-header-footer` and CSS `print-color-adjust:exact`
  → no browser headers, backgrounds preserved.

## Workflow

1. **Prepare assets** (font + any images) as base64. Use the helper:
   ```bash
   python3 .claude/skills/persian-pdf/scripts/prepare_assets.py
   ```
   This ensures the Vazirmatn TTFs exist at `/tmp/Vazirmatn-{Regular,Bold}.ttf`
   (downloading from GitHub raw if missing) and prints their base64 to
   `/tmp/vazir_reg_b64.txt` and `/tmp/vazir_bold_b64.txt`.

   For an image (e.g. a profile photo cropped from a screenshot), use Pillow to
   crop/resize then base64-encode it — embed with `src="data:image/jpeg;base64,..."`.

2. **Write the HTML.** Start from `assets/template.html` (a full A4 RTL skeleton
   with the `@font-face` blocks, `@page{size:A4;margin:0}`, and
   `print-color-adjust:exact` already wired). Key rules:
   - `<html lang="fa" dir="rtl">`
   - Embed fonts via `@font-face { src:url(data:font/ttf;base64,...) }` — paste the
     base64 from step 1 (do NOT rely on a web CDN; jsdelivr is often blocked).
   - Use real Persian digits (۰۱۲۳۴۵۶۷۸۹) and the thousands separator `٬` in text.
   - For half/full stars etc., use spans + CSS, not unicode glyphs that the font
     may lack.
   - Multi-page: each page is `<div class="page">`; they flow automatically onto
     separate A4 sheets.

3. **Render to PDF** with the helper (it auto-locates Chromium):
   ```bash
   python3 .claude/skills/persian-pdf/scripts/html_to_pdf.py input.html output.pdf
   ```

4. **Verify visually** — render a screenshot and Read it before delivering:
   ```bash
   python3 .claude/skills/persian-pdf/scripts/html_to_pdf.py input.html /tmp/preview.png --screenshot
   ```
   Then use the Read tool on `/tmp/preview.png` to confirm there are no `□` boxes,
   text isn't clipped, and RTL alignment is correct. Fix and re-render if needed.

5. **Deliver** the `.pdf` with SendUserFile. Commit the `.html` + `.pdf` if the
   user wants them in the repo.

## Notes / gotchas

- Run Bash with `dangerouslyDisableSandbox: true` for the render/download steps —
  the sandbox blocks the font download and Chromium needs `--no-sandbox`.
- If Chromium isn't at the Playwright path, the helper falls back to
  `chromium`/`google-chrome` on PATH, or `npx puppeteer browsers install chrome`.
- Embedding fonts makes the HTML large (~350 KB+). That's expected and fine.
- The same pipeline works for LTR/English docs — just set `dir="ltr"` and you can
  keep or drop the Persian font.

See `reference.md` for the design-language cheatsheet (colors, cards, tables,
signature blocks, stat tiles) used to make documents look professional.
