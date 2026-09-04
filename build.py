#!/usr/bin/env python3
"""Assemble the HOH 3015 companion text from its chapter fragments.

    python3 build.py

Reads  vtsu/book/src/ch-0N.html and vtsu/assets/figures/*.svg
Writes vtsu/book/index.html, one self contained file that opens from disk.
"""
import html, pathlib, re, sys

HERE = pathlib.Path(__file__).parent
SRC = HERE / "src"
FIGDIR = HERE / "assets" / "figures"

WEEK = {1: "Week one", 2: "Week two", 3: "Week three", 4: "Week four",
        5: "Week five", 6: "Week six", 7: "Week seven"}
COLOR = {1: "var(--fig-brand,#0f5f66)", 2: "var(--fig-brand,#0f5f66)",
         3: "var(--fig-accent,#a95a22)", 4: "var(--fig-accent,#a95a22)",
         5: "var(--u3,#7a5ea8)", 6: "var(--u3,#7a5ea8)", 7: "var(--u3,#7a5ea8)"}

FIGS = {f.stem: f.read_text().strip() for f in FIGDIR.glob("fig-*.svg")}
USED = []


def inject_figures(markup, where):
    missing = []

    def sub(m):
        fid = m.group(1)
        USED.append(fid)
        svg = FIGS.get(fid)
        if svg is None:
            missing.append(fid)
            return m.group(0)
        return m.group(0) + "\n      " + svg

    out = re.sub(r'<figure class="ch-fig" data-fig="([^"]+)">', sub, markup)
    if missing:
        sys.exit("%s: no drawing for %s" % (where, missing))
    return out


def plate(n):
    """Chapter opener: the numeral, the week, and seven segments with this one lit."""
    c = COLOR[n]
    segs = []
    for i in range(1, 8):
        x = 300 + (i - 1) * 56
        here = i == n
        w, h = (34, 17) if here else (26, 11)
        y = 60 - h / 2
        segs.append(
            '<rect x="%.0f" y="%.0f" width="%d" height="%d" rx="%.0f" fill="%s" opacity="%s"/>'
            % (x - w / 2, y, w, h, h / 2, c if here else "currentColor", 1 if here else 0.2))
        if here:
            segs.append('<text x="%.0f" y="94" text-anchor="middle" font-size="11" fill="%s" '
                        'font-weight="700">%02d</text>' % (x, c, n))
    return (
        '<svg class="ch-plate" viewBox="0 0 720 116" role="img" '
        'aria-label="Chapter %d of 7, read in %s of the session.">'
        '<g font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif">'
        '<text x="0" y="74" font-size="58" font-weight="600" fill="%s" '
        'font-family="Iowan Old Style, Palatino Linotype, Palatino, Georgia, serif" '
        'opacity=".95">%02d</text>'
        '<text x="0" y="98" font-size="10.5" letter-spacing="1.6" fill="currentColor" '
        'opacity=".55">%s</text>'
        '<line x1="270" y1="26" x2="270" y2="94" stroke="currentColor" opacity=".2"/>'
        '%s</g></svg>'
        % (n, WEEK[n].lower(), c, n, WEEK[n].upper(), "".join(segs)))


def main():
    frags = sorted(SRC.glob("ch-*.html"))
    if len(frags) != 7:
        sys.exit("expected 7 chapters in src, found %d" % len(frags))

    chapters, toc, total = [], [], 0
    for i, f in enumerate(frags, 1):
        s = f.read_text().strip()
        m = re.search(r'data-title="([^"]+)"', s)
        title = m.group(1) if m else "Chapter %02d" % i
        words = len(html.unescape(re.sub(r"<[^>]+>", " ", s)).split())
        total += words
        s = inject_figures(s, f.name)
        s = s.replace('<p class="ch-num">', plate(i) + '\n  <p class="ch-num">', 1)
        chapters.append(s)
        toc.append((i, title, max(1, round(words / 220))))

    toc_html = "\n".join(
        '      <li><button class="toc-item" data-go="%d">'
        '<span class="toc-n">%02d</span>'
        '<span class="toc-t">%s<span class="toc-m">%s &middot; %d min read</span></span>'
        '<span class="toc-dot" aria-hidden="true"></span></button></li>'
        % (i, i, html.escape(t), WEEK[i], m) for i, t, m in toc)

    tpl = (HERE / "template.html").read_text()
    out = (tpl.replace("<!--COVER-->", (HERE / "cover.svg").read_text().strip())
              .replace("<!--TOC-->", toc_html)
              .replace("<!--CHAPTERS-->", "\n".join(chapters))
              .replace("/*--FIGCSS--*/", (FIGDIR / "figures.css").read_text())
              .replace("/*--FIGJS--*/", (FIGDIR / "figures.js").read_text())
              .replace("__FIGS__", str(len(set(USED))))
              .replace("__WORDS__", "%dk" % round(total / 1000)))
    (HERE / "index.html").write_text(out)

    print("book/index.html  7 chapters, %s words, %d figures placed (%d distinct), %d KB"
          % ("{:,}".format(total), len(USED), len(set(USED)), len(out) // 1024))
    for i, t, m in toc:
        print("   %02d  %-46s %2d min" % (i, t[:46], m))


if __name__ == "__main__":
    main()
