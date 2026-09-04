#!/usr/bin/env python3
"""Build the print edition of the companion text: one flowing document, all seven
chapters, figures inlined at their finished state, sized for US Letter.

    python3 build-print.py      writes vtsu/book/print.html
    (then Playwright renders it to vtsu/book/HOH3015_Companion_Text.pdf)
"""
import html, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
SRC = HERE / "src"
FIGDIR = HERE / "assets" / "figures"
FIGS = {f.stem: f.read_text().strip() for f in FIGDIR.glob("fig-*.svg")}

WEEK = {1: "Week one", 2: "Week two", 3: "Week three", 4: "Week four",
        5: "Week five", 6: "Week six", 7: "Week seven"}

CSS = """
@page { size: letter; margin: 0.85in 0.9in 1in 0.9in; }
:root{ --ink:#1b2430; --ink2:#39424f; --muted:#5f6b78; --line:#ddd6c8;
  --brand:#0f5f66; --accent:#a95a22;
  --fig-accent:#a95a22; --fig-brand:#0f5f66; --fig-warn:#b4423a;
  --fig-mute:#7c8894; --fig-fill:rgba(27,36,48,.06); --u3:#7a5ea8;
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;
  --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; }
*{box-sizing:border-box}
body{margin:0;color:var(--ink);background:#fff;font-family:var(--serif);
  font-size:10.8pt;line-height:1.55;-webkit-print-color-adjust:exact;print-color-adjust:exact}
p{margin:0 0 .62em;text-align:justify;hyphens:none;orphans:2;widows:2}

.title-page{height:9in;display:flex;flex-direction:column;justify-content:center;
  page-break-after:always;text-align:center}
.title-page .kick{font-family:var(--mono);font-size:8pt;letter-spacing:.22em;
  text-transform:uppercase;color:var(--accent);margin:0 0 14px}
.title-page h1{font-size:30pt;margin:0 0 10px;font-weight:600;letter-spacing:-.01em}
.title-page p{text-align:center}
.title-page .sub{font-family:var(--sans);font-size:11pt;color:var(--muted);margin:0 0 4px}
.title-page .rule{width:70px;height:2px;background:var(--ink);margin:22px auto}
.title-page .cover-art{display:block;width:4.4in;margin:26px auto 0;color:var(--ink)}
.title-page .cover-art .cov-hit{display:none}

.toc-page{page-break-after:always}
.toc-page h2{font-size:15pt;color:var(--brand);margin:0 0 18px;font-weight:600}
.toc-row{display:flex;gap:12px;align-items:baseline;padding:9px 0;border-bottom:1px solid var(--line);
  font-family:var(--sans);font-size:10pt}
.toc-row .n{font-family:var(--mono);font-size:8.5pt;color:var(--accent);width:22px}
.toc-row .t{flex:1;color:var(--ink)}
.toc-row .w{color:var(--muted);font-size:8.5pt}

.chap{page-break-before:always}
.ch-plate{display:none}
.ch-num{font-family:var(--mono);font-size:8pt;letter-spacing:.2em;text-transform:uppercase;
  color:var(--accent);margin:0 0 4px}
.chap h2{font-size:19pt;margin:0 0 10px;font-weight:600;line-height:1.2;letter-spacing:-.01em;
  page-break-after:avoid}
.ch-hook{font-style:italic;color:var(--ink2);font-size:11.6pt;line-height:1.45;
  border-left:3px solid var(--accent);padding:2px 0 2px 14px;margin:0 0 18px;text-align:left}
.chap h3{font-family:var(--sans);font-size:11pt;font-weight:700;color:var(--brand);
  margin:20px 0 7px;page-break-after:avoid;text-align:left}

.ch-fig{margin:16px 0 18px;padding:0;page-break-inside:avoid}
.ch-fig svg{display:block;width:100%;height:auto;max-height:4.2in;color:var(--ink)}
.ch-fig figcaption{font-family:var(--sans);font-size:8.6pt;line-height:1.45;color:var(--muted);
  margin-top:7px;padding-top:7px;border-top:1px solid var(--line);text-align:left}
.fig-controls,.fig-readout{display:none}

.ch-pull{font-family:var(--sans);font-size:12pt;line-height:1.4;font-weight:600;color:var(--brand);
  border-top:2px solid var(--line);border-bottom:2px solid var(--line);padding:13px 0;
  margin:20px 0;text-align:left;page-break-inside:avoid}
.ch-note{background:#faf7f1;border:1px solid var(--line);border-left:3px solid var(--accent);
  border-radius:0 5px 5px 0;padding:13px 16px;margin:16px 0;page-break-inside:avoid}
.ch-note h3{margin:0 0 6px;font-size:9.5pt;color:var(--accent)}
.ch-note p{margin:0 0 .5em;font-size:10pt}
.ch-note p:last-child{margin:0}

.ch-terms,.ch-check{border-top:2px solid var(--ink);padding-top:12px;margin-top:26px;
  page-break-inside:avoid}
.ch-terms h3,.ch-check h3{margin:0 0 10px;font-size:10.5pt;color:var(--ink)}
.ch-terms dl{margin:0;font-size:9.8pt}
.ch-terms dt{font-weight:700;color:var(--brand);margin-top:8px}
.ch-terms dd{margin:1px 0 0;color:var(--ink2)}
.ch-check ol{margin:0;padding-left:20px;font-size:9.8pt;color:var(--ink2)}
.ch-check li{margin-bottom:6px}
ul,ol{margin:0 0 .7em;padding-left:22px}
li{margin-bottom:4px}
strong{color:var(--ink)}
em{font-style:italic}
"""


def main():
    frags = sorted(SRC.glob("ch-*.html"))
    if len(frags) != 7:
        sys.exit("expected 7 chapters, found %d" % len(frags))

    chapters, toc = [], []
    for i, f in enumerate(frags, 1):
        s = f.read_text().strip()
        m = re.search(r'data-title="([^"]+)"', s)
        toc.append((i, m.group(1) if m else "Chapter %d" % i))
        missing = []

        def sub(mm):
            fid = mm.group(1)
            svg = FIGS.get(fid)
            if svg is None:
                missing.append(fid)
                return mm.group(0)
            # print edition shows the finished drawing: strip the interaction attributes
            svg = re.sub(r'\sdata-(steps|layers|only|pulse|step|layer|hot|tip)="[^"]*"', "", svg)
            return mm.group(0) + "\n" + svg

        s = re.sub(r'<figure class="ch-fig" data-fig="([^"]+)">', sub, s)
        if missing:
            sys.exit("chapter %d: no drawing for %s" % (i, missing))
        chapters.append(s)

    toc_html = "\n".join(
        '<div class="toc-row"><span class="n">%02d</span>'
        '<span class="t">%s</span><span class="w">%s</span></div>'
        % (i, html.escape(t), WEEK[i]) for i, t in toc)

    cover = (HERE / "cover.svg").read_text().strip()
    out = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>The Spine You Will Touch</title>
<style>%s</style></head><body>

<div class="title-page">
  <p class="kick">Companion text</p>
  <h1>The Spine You Will Touch</h1>
  <div class="rule"></div>
  <p class="sub">The reading for HOH 3015</p>
  <p class="sub">Chiropractic History, Theory, and Practice</p>
  <p class="sub" style="margin-top:22px">Akash Garg, D.C.</p>
  <p class="sub">Vermont State University &middot; VTSU Online</p>
  <p class="sub">Fall 2026, session 7B</p>
  %s
</div>

<div class="toc-page">
  <h2>Contents</h2>
  %s
  <p style="font-family:var(--sans);font-size:9pt;color:var(--muted);margin-top:26px;text-align:left">
  This is the print edition. The diagrams in the online reader can be stepped through, switched
  between layers, and hovered for detail. Here they are shown in their finished state. If a figure
  looks dense on the page, open the same figure in the Canvas reader and take it apart.</p>
</div>

%s
</body></html>""" % (CSS, cover, toc_html, "\n".join(chapters))

    (HERE / "print.html").write_text(out)
    words = len(html.unescape(re.sub(r"<svg.*?</svg>", " ", out, flags=re.S)
                              .replace("<", " <")).split())
    print("book/print.html  7 chapters, %d KB" % (len(out) // 1024))


if __name__ == "__main__":
    main()
