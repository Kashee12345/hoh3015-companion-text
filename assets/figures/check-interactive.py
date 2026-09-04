#!/usr/bin/env python3
"""Validate the interactive annotations on every figure."""
import glob, json, re, sys, xml.dom.minidom, pathlib

HERE = pathlib.Path(__file__).parent
BAD = re.compile(r"[-‐-―−]")


def main():
    errs, rows = [], []
    for f in sorted(glob.glob(str(HERE / "*.svg"))):
        name = pathlib.Path(f).name
        s = pathlib.Path(f).read_text()
        try:
            xml.dom.minidom.parseString(s)
        except Exception as e:
            errs.append(f"{name}: NOT VALID XML: {e}")
            continue

        steps = re.search(r"data-steps='([^']*)'", s)
        layers = re.search(r"data-layers='([^']*)'", s)
        nstep = nlayer = 0
        strings = []

        if steps:
            try:
                v = json.loads(steps.group(1))
                nstep = len(v)
                strings += v
                if not 2 <= nstep <= 6:
                    errs.append(f"{name}: {nstep} steps, want 2 to 6")
            except Exception as e:
                errs.append(f"{name}: data-steps is not valid JSON: {e}")
            used = sorted({int(x) for x in re.findall(r'data-step="(\d+)"', s)})
            if used and max(used) > nstep:
                errs.append(f"{name}: data-step={max(used)} but only {nstep} steps declared")
            missing = [i for i in range(1, nstep + 1) if i not in used]
            if missing:
                errs.append(f"{name}: no element assigned to step(s) {missing}")
        elif re.search(r'data-step="', s):
            errs.append(f"{name}: elements carry data-step but the svg declares no data-steps")

        if layers:
            try:
                v = json.loads(layers.group(1))
                nlayer = len(v)
                strings += [x.get("label", "") for x in v] + [x.get("note", "") for x in v]
                keys = {x["k"] for x in v}
                used = set(re.findall(r'data-layer="([^"]+)"', s))
                if used - keys:
                    errs.append(f"{name}: data-layer {sorted(used - keys)} not declared")
                for k in keys:
                    if k not in used:
                        errs.append(f"{name}: layer '{k}' declared but no element uses it")
            except Exception as e:
                errs.append(f"{name}: data-layers is not valid JSON: {e}")

        hots = re.findall(r'data-hot="([^"]*)"', s)
        tips = re.findall(r'data-tip="([^"]*)"', s)
        strings += hots + tips
        if len(hots) != len(tips):
            errs.append(f"{name}: {len(hots)} data-hot but {len(tips)} data-tip")

        if not (nstep or nlayer or hots):
            errs.append(f"{name}: NOT INTERACTIVE, no steps, layers or hotspots")

        for t in strings:
            if BAD.search(t):
                errs.append(f"{name}: dash in player facing string: {t[:70]!r}")
            if any(ord(c) > 127 for c in t):
                errs.append(f"{name}: non ascii in string: {t[:50]!r}")

        if 'role="img"' not in s or "aria-label" not in s:
            errs.append(f"{name}: lost role or aria-label")
        if re.search(r'data-(pulse|only)(?![=])', s):
            errs.append(f"{name}: bare data-pulse or data-only, write it as =\"\"")

        rows.append((name, nstep, nlayer, len(hots)))

    w = max(len(r[0]) for r in rows) if rows else 10
    for name, a, b, c in rows:
        flag = " " if (a or b or c) else "!"
        print(f"{flag} {name:<{w}}  steps {a}  layers {b}  hotspots {c}")
    print()
    for e in errs:
        print("ERROR", e)
    print(f"\n{len(rows)} figures, {sum(1 for r in rows if r[1] or r[2] or r[3])} interactive")
    print("ALL OK" if not errs else f"{len(errs)} ERRORS TO FIX")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
