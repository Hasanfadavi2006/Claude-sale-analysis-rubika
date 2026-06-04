# Design cheatsheet — making documents look professional

Reusable CSS patterns proven to render cleanly in Chromium-to-PDF for Persian/RTL
documents. Mix and match.

## Color palettes (pick one per document)

| Mood | --brand | --brand2 | accent |
|---|---|---|---|
| Corporate navy/teal (reports) | `#123a5e` | `#1f6f8b` | `#15784e` |
| Trustworthy green (receipts) | `#1a7a3c` | `#2bb673` | gold `#f5a623` |
| Neutral slate (forms) | `#33415c` | `#5f6b7a` | `#1d9bf0` |

Always set on the document:
```css
-webkit-print-color-adjust:exact; print-color-adjust:exact;
@page{size:A4;margin:0;}
```

## Building blocks

**Side accent bar** (subtle "designed" feel):
```html
<div class="edge"></div>  <!-- absolute, full-height, 6mm, gradient -->
```

**Section heading with bar:**
```html
<h2 class="h-sec"><span class="bar"></span>عنوان بخش</h2>
```

**Stat tiles** (big numbers):
```html
<div class="grid3">
  <div class="stat"><div class="num">۲٬۰۲۰</div><div class="lbl">توضیح</div></div>
</div>
```
```css
.stat{text-align:center;border:1px solid var(--line);border-radius:12px;
  padding:10px 6px;background:var(--soft);}
.stat .num{font-size:20px;font-weight:800;color:var(--brand2);}
.stat .lbl{font-size:10px;color:var(--muted);margin-top:2px;}
```

**Info cards grid:**
```css
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:11px;}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;}
.card{border:1px solid var(--line);border-radius:11px;padding:11px 13px;}
.card .k{font-size:10.5px;color:var(--muted);font-weight:700;}
.card .v{font-size:12px;font-weight:700;margin-top:2px;}
```

**Callout / note box** (variants: add `.ok` green, `.warn` gold):
```css
.callout.ok{border-right-color:var(--ok);background:#eef7f1;}
.callout.warn{border-right-color:var(--gold);background:#fdf8ee;}
```

**Avatar with verified badge** (for people/providers):
```css
.avatar{width:90px;height:90px;border-radius:50%;object-fit:cover;
  border:3px solid #fff;box-shadow:0 4px 12px rgba(0,0,0,.18);}
.verified{position:absolute;bottom:2px;left:2px;width:26px;height:26px;
  background:#1d9bf0;color:#fff;border:3px solid #fff;border-radius:50%;
  display:flex;align-items:center;justify-content:center;}
```

**Half-star rating** (don't trust a single unicode half-star glyph):
```html
<span class="stars">
  <span class="s full">★</span>...<span class="s half">★</span>
</span>
```
```css
.stars .s{position:relative;color:#d8dde5;}
.stars .s.full{color:var(--gold);}
.stars .s.half::before{content:"★";position:absolute;right:0;top:0;
  width:50%;overflow:hidden;color:var(--gold);}
```

**Signature blocks** (for documents that get signed):
```css
.sign{flex:1;border:1.5px dashed #c7cdd6;border-radius:13px;padding:16px;
  text-align:center;min-height:120px;display:flex;flex-direction:column;
  justify-content:space-between;}
.sign .ln{margin-top:auto;border-top:1.5px solid #cfd6e0;padding-top:8px;
  color:var(--muted);}
```

**Pricing total bar** (receipts/invoices):
```css
.price{display:flex;align-items:center;justify-content:space-between;
  background:linear-gradient(100deg,var(--brand),var(--brand2));color:#fff;
  border-radius:13px;padding:14px 18px;}
.price .amt{font-size:22px;font-weight:800;}
```

## Persian typography rules

- Digits: use ۰۱۲۳۴۵۶۷۸۹ (not 0-9) in body text.
- Thousands separator: `٬` (e.g. ۱۵٬۸۰۰٬۰۰۰).
- Decimal: `٫` (e.g. ۴٫۵).
- `text-align:justify` reads well for Persian paragraphs.
- Keep Latin terms (API, CRM, HP DL380) as-is inside RTL — Chromium shapes the
  bidi correctly.

## Multi-page documents

- Each `<div class="page">` becomes one A4 sheet automatically.
- Put a cover page first (centered flex column), then a TOC/summary page, then
  content pages. Add a page number + footer absolutely-positioned per page.
- Keep tables from splitting awkwardly: `tr{break-inside:avoid;}`.

## Verify before delivering

Always screenshot and Read it:
```
python3 scripts/html_to_pdf.py doc.html /tmp/preview.png --screenshot
```
Check for: □ boxes (font missing), clipped text, wrong RTL alignment, colors
dropped (means `print-color-adjust:exact` missing).
