#!/usr/bin/env python3
"""Draw the cover: a lateral spine, anatomically shaped, whose seven marked
vertebrae are the table of contents. Click one and the reader opens that chapter.

    python3 make-cover.py       writes vtsu/book/cover.svg
"""
import math, pathlib

W, H = 660, 740

# Centerline control points, anterior to the right. Occiput at the top, sacrum
# at the bottom, with the four alternating curves: cervical lordosis, thoracic
# kyphosis, lumbar lordosis, sacral kyphosis.
CTRL = [
    (206, 54),    # base of skull
    (220, 116),   # cervical lordosis, apex forward
    (212, 182),   # cervicothoracic junction
    (188, 272),
    (180, 350),   # thoracic kyphosis, apex back
    (196, 456),   # thoracolumbar junction
    (214, 528),   # lumbar lordosis, apex forward
    (204, 592),   # lumbosacral junction
    (178, 672),   # sacrum, tilting back
]


def catmull(pts, n):
    """Sample a Catmull Rom spline through pts, returning n points."""
    p = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    segs = len(p) - 3
    for i in range(n):
        t = i / (n - 1) * segs
        k = min(int(t), segs - 1)
        u = t - k
        p0, p1, p2, p3 = p[k], p[k + 1], p[k + 2], p[k + 3]
        u2, u3 = u * u, u * u * u
        x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * u
                   + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * u2
                   + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * u3)
        y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * u
                   + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * u2
                   + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * u3)
        out.append((x, y))
    return out


# 24 mobile vertebrae, C1 at the top through L5, then the sacrum as a wedge.
N = 24
PATH = catmull(CTRL, 400)


# cumulative arc length, so a fraction means a fraction of the DISTANCE travelled
# rather than a fraction of the spline parameter. Without this the vertebrae bunch
# wherever the control points sit close together.
_ARC = [0.0]
for _a, _b in zip(PATH, PATH[1:]):
    _ARC.append(_ARC[-1] + math.hypot(_b[0] - _a[0], _b[1] - _a[1]))
_TOTAL = _ARC[-1]


def at(frac):
    """Point and tangent angle at a fraction of the arc length."""
    target = max(0.0, min(1.0, frac)) * _TOTAL
    lo, hi = 0, len(_ARC) - 1
    while lo < hi - 1:
        mid = (lo + hi) // 2
        if _ARC[mid] <= target:
            lo = mid
        else:
            hi = mid
    i = max(1, min(len(PATH) - 2, lo))
    span = _ARC[i + 1] - _ARC[i] or 1.0
    u = (target - _ARC[i]) / span
    x = PATH[i][0] + (PATH[i + 1][0] - PATH[i][0]) * u
    y = PATH[i][1] + (PATH[i + 1][1] - PATH[i][1]) * u
    dx = PATH[i + 1][0] - PATH[i - 1][0]
    dy = PATH[i + 1][1] - PATH[i - 1][1]
    return x, y, math.degrees(math.atan2(dy, dx)) - 90


# Chapter markers: which vertebra index (0 based, C1 = 0) carries each chapter.
CHAPTERS = [
    (1, 1, "Origins and First Principles", "Week one"),
    (2, 5, "The Spine You Will Touch", "Week two"),
    (3, 9, "The Art of Technique", "Week three"),
    (4, 13, "Becoming One", "Week four"),
    (5, 17, "In the Clinic", "Week five"),
    (6, 20, "Alongside Everyone Else", "Week six"),
    (7, 23, "What You Do With This", "Week seven"),
]
MARKED = {v: (n, t, w) for n, v, t, w in CHAPTERS}


def vertebra(i):
    """One vertebra: body anterior, spinous process posterior and angled down.
    Cervical small with a short spinous, thoracic with a long downward spinous,
    lumbar large with a broad horizontal one."""
    frac = 0.028 + (i / (N - 1)) * 0.730
    x, y, rot = at(frac)

    # body grows going down: cervical narrow, lumbar wide
    t = i / (N - 1)
    bw = 15 + 16 * t          # body width, anterior to posterior on the drawing
    bh = 8.2 + 3.6 * t        # body height, kept under the spacing so discs show
    if i < 7:                 # cervical
        sp_len, sp_drop, sp_w = 12, 2, 2.8
    elif i < 19:              # thoracic, long spinous angled down
        sp_len, sp_drop, sp_w = 20 + 7 * ((i - 7) / 11), 11, 3.0
    else:                     # lumbar, broad and near horizontal
        sp_len, sp_drop, sp_w = 19, 1, 4.8

    marked = i in MARKED
    body_fill = "var(--fig-accent,#a95a22)" if marked else "var(--fig-fill,rgba(127,127,127,.10))"
    body_op = "0.90" if marked else "1"
    stroke = "var(--fig-accent,#a95a22)" if marked else "currentColor"
    sw = "1.6" if marked else "1"
    op = "1" if marked else ".62"

    g = ['<g transform="translate(%.1f %.1f) rotate(%.1f)" opacity="%s">' % (x, y, rot, op)]
    # body
    g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="%s" '
             'fill-opacity="%s" stroke="%s" stroke-width="%s"/>'
             % (-bw * 0.30, -bh / 2, bw, bh, bh * 0.34, body_fill, body_op, stroke, sw))
    # spinous process, pointing posteriorly (to the left) and down
    g.append('<path d="M %.1f %.1f L %.1f %.1f" stroke="%s" stroke-width="%.1f" '
             'stroke-linecap="round" fill="none"/>'
             % (-bw * 0.30, 0, -bw * 0.30 - sp_len, sp_drop, stroke, sp_w))
    g.append("</g>")
    return "".join(g), x, y


def build():
    parts = []

    # sacrum and coccyx as one tapering wedge below L5
    sx, sy, srot = at(0.795)
    parts.append(
        '<g transform="translate(%.1f %.1f) rotate(%.1f)" opacity=".55">'
        '<path d="M -13 -6 L 17 -6 L 11 44 L 1 62 L -9 42 Z" '
        'fill="var(--fig-fill,rgba(127,127,127,.10))" stroke="currentColor" stroke-width="1"/>'
        '<path d="M -8 6 L 12 6 M -7 18 L 10 18 M -5 30 L 8 30" stroke="currentColor" '
        'stroke-width=".7" opacity=".5"/></g>' % (sx, sy, srot))

    # the vertebrae, unmarked first so the marked ones sit on top
    marks = {}
    plain, lit = [], []
    for i in range(N):
        svg, x, y = vertebra(i)
        (lit if i in MARKED else plain).append(svg)
        if i in MARKED:
            marks[i] = (x, y)
    parts += plain + lit

    # skull suggestion at the top, cropped by the frame
    parts.append('<path d="M 188 46 Q 196 20 224 21 Q 248 22 252 42" fill="none" '
                 'stroke="currentColor" stroke-width="1" opacity=".2"/>')

    # lead lines and chapter labels, to the right
    label_x = 300
    MIN_GAP = 78
    prev_ly = None
    for n, vi, title, week in CHAPTERS:
        x, y = marks[vi]
        ly = y + 5
        if prev_ly is not None and ly - prev_ly < MIN_GAP:
            ly = prev_ly + MIN_GAP
        prev_ly = ly
        parts.append(
            '<g class="cov-ch" data-go="%d" data-label="Chapter %d, %s, %s">'
            % (n, n, title, week.lower()))
        parts.append('<rect class="cov-hit" x="%d" y="%.1f" width="330" height="46" rx="7" '
                     'fill="transparent"/>' % (label_x - 16, ly - 31))
        parts.append('<path class="cov-lead" d="M %.1f %.1f L %.1f %.1f L %d %.1f" '
                     'fill="none" stroke="currentColor" stroke-width="1" opacity=".28"/>'
                     % (x + 17, y, label_x - 42, ly - 5, label_x - 20, ly - 5))
        parts.append('<circle class="cov-dot" cx="%.1f" cy="%.1f" r="2.6" '
                     'fill="var(--fig-accent,#a95a22)"/>' % (x + 16, y))
        parts.append('<text class="cov-n" x="%d" y="%.1f" font-size="10" '
                     'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
                     'letter-spacing="1.4" fill="var(--fig-accent,#a95a22)">%02d    %s</text>'
                     % (label_x, ly - 15, n, week.upper()))
        parts.append('<text class="cov-t" x="%d" y="%.1f" font-size="15.5" '
                     'font-family="Iowan Old Style, Palatino Linotype, Palatino, Georgia, serif" '
                     'fill="currentColor">%s</text>' % (label_x, ly + 5, title))
        parts.append("</g>")

    svg = (
        '<svg class="cover-art" viewBox="156 26 %d %d" role="img" '
        'aria-label="The seven chapters of the book laid along a drawing of the spine seen from '
        'the side, each chapter marked at a vertebra. Select a chapter to open it.">'
        '<g font-family="system-ui, -apple-system, Segoe UI, Roboto, sans-serif">'
        '%s</g></svg>' % (W - 176, H - 66, "".join(parts)))
    pathlib.Path(__file__).parent.joinpath("cover.svg").write_text(svg)
    print("cover.svg  %d vertebrae, %d chapter markers, %d bytes"
          % (N, len(CHAPTERS), len(svg)))


if __name__ == "__main__":
    build()
