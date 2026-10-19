#!/usr/bin/env python3
"""Flatten the bible (02, 03, 04, 08) into index.json and index-stats.txt, and check it.

  python3 -I tools/build_index.py [--root DIR]

DIR is the lore folder, the one holding lore.toml (default: the folder above tools/).
Stdlib only, Python 3.11+. Idempotent: re-run after every edit to bible/ or refs/.
Errors (the markdown breaks FORMAT.md) exit 1; warnings go to index-stats.txt.
"""
import argparse
import json
import os
import re
import sys
import tomllib

ENTRY_FILES = ["02", "03", "04", "08"]
IMG = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
KEYS = {"slug", "aliases", "what", "appears", "tier", "maps-to", "visual", "lighting",
        "refs", "quotes", "source", "who", "where", "tone", "follows", "weight"}
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FILE_MAX_LINES = 700


def slugify(s):
    s = s.lower().replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def split_list(s):
    return [x.strip() for x in s.split(",") if x.strip()]


def load_config(root):
    path = os.path.join(root, "lore.toml")
    if not os.path.isfile(path):
        sys.exit("no lore.toml in %s (pass --root, or copy the kit's lore.toml there)" % root)
    with open(path, "rb") as fh:
        cfg = tomllib.load(fh)
    project = cfg.get("project", {})
    if project.get("mode") not in ("adaptation", "original"):
        sys.exit("lore.toml: project.mode is %r; set it to \"adaptation\" or \"original\" (the lore-setup skill does this)"
                 % project.get("mode"))
    return cfg


def bible_files(root):
    """{"00": "00 index.md", ...} for every numbered markdown file in bible/."""
    out = {}
    d = os.path.join(root, "bible")
    if os.path.isdir(d):
        for fn in sorted(os.listdir(d)):
            m = re.match(r"^(\d\d) .+\.md$", fn)
            if m and m.group(1) not in out:
                out[m.group(1)] = fn
    return out


def kind_for(kinds, heading):
    h = heading.lower()
    for kw, kind in kinds:
        if kw in h:
            return kind
    return None


def parse_entries(root, name, fileno, cfg, unit_re, errors):
    rows = []
    section, kind, unit, cur = "", None, "", None
    kinds = cfg.get("kinds", {}).get(fileno, [])
    with open(os.path.join(root, "bible", name), encoding="utf-8") as fh:
        lines = fh.read().split("\n")

    def close():
        nonlocal cur
        if cur is not None:
            rows.append(cur)
            cur = None

    for n, line in enumerate(lines, 1):
        where = "%s:%d" % (name, n)
        if line.startswith("### "):
            close()
            cur = {"_name": line[4:].strip(), "_kind": kind, "_section": section, "_unit": unit,
                   "_file": name, "_line": n, "_f": {}}
            if kind is None:
                errors.append("%s: entry '%s' is under a heading with no kind (see [kinds] in lore.toml)" % (where, cur["_name"]))
            continue
        if line.startswith("#"):
            close()
            section = line.lstrip("#").strip()
            if fileno == "08":
                kind = "moment"
                if line.startswith("## "):
                    m = unit_re.search(section) if unit_re else None
                    unit = m.group(0) if m else ("" if unit_re else section)
            else:
                k = kind_for(kinds, section)
                if k:
                    kind = k
            continue
        if cur is None or not line.strip():
            continue
        m = re.match(r"^- ([a-z-]+): ?(.*)$", line)
        if not m:
            errors.append("%s: unparseable line in '%s': %r" % (where, cur["_name"], line[:80]))
            continue
        key, val = m.group(1), m.group(2).strip()
        if key not in KEYS:
            errors.append("%s: unknown key '%s' in '%s'" % (where, key, cur["_name"]))
        elif key in cur["_f"]:
            errors.append("%s: duplicate key '%s' in '%s'" % (where, key, cur["_name"]))
        else:
            cur["_f"][key] = val
    close()
    return rows


def parse_outline(root, name, unit_re):
    """Unit codes from 01, in order."""
    units = []
    if not name or not unit_re:
        return units
    with open(os.path.join(root, "bible", name), encoding="utf-8") as fh:
        for line in fh:
            m = unit_re.match(line.strip())
            if m and " · " in line:
                units.append(m.group(0))
    return units


def check_voice(root, name, line_max, errors):
    if not name:
        return 0
    flagged = 0
    with open(os.path.join(root, "bible", name), encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            if not re.search(r"·\s*SHORT\s*$", line):
                continue
            flagged += 1
            m = re.search(r"[\"“](.+?)[\"”]", line)
            if not m:
                errors.append("%s:%d: SHORT line has no quoted text" % (name, n))
            elif len(m.group(1)) > line_max:
                errors.append("%s:%d: SHORT line is %d characters, the limit is %d" % (name, n, len(m.group(1)), line_max))
    return flagged


def list_images(folder):
    if not os.path.isdir(folder):
        return []
    return [os.path.join(folder, fn) for fn in sorted(os.listdir(folder), key=lambda x: (len(x), x))
            if os.path.splitext(fn)[1].lower() in IMG]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    root = os.path.abspath(ap.parse_args().root)
    cfg = load_config(root)
    project = cfg["project"]
    visual = project.get("visual", True)
    pattern = cfg.get("units", {}).get("pattern", "")
    unit_re = re.compile(pattern) if pattern else None
    tiers = cfg.get("tiers", {}).get("values", ["iconic", "known", "deep-cut"])
    top_tiers = tiers[:2]
    gap_min = cfg.get("tiers", {}).get("gap_min_refs", 3)
    tones = set(cfg.get("moments", {}).get("tones", []))
    line_max = cfg.get("voice", {}).get("line_max", 90)

    files = bible_files(root)
    errors, warnings = [], []
    raw = []
    for no in ENTRY_FILES:
        if no in files:
            raw.extend(parse_entries(root, files[no], no, cfg, unit_re, errors))
    outline = parse_outline(root, files.get("01"), unit_re)
    flagged = check_voice(root, files.get("06"), line_max, errors)

    required = ["slug", "what", "tier", "maps-to", "source"]
    if visual:
        required.append("visual")

    rows, seen = [], {}
    for e in raw:
        f = e["_f"]
        where = "%s:%d" % (e["_file"], e["_line"])
        is_moment = e["_kind"] == "moment"
        need = required + (["who", "tone", "weight"] if is_moment else [])
        if unit_re and not is_moment:
            need = need + ["appears"]
        for k in need:
            if not f.get(k):
                errors.append("%s: '%s' is missing '%s'" % (where, e["_name"], k))
        tier = f.get("tier", "")
        if tier and tier not in tiers:
            errors.append("%s: '%s' has tier %r, expected one of %s" % (where, e["_name"], tier, ", ".join(tiers)))
        slug = f.get("slug", "")
        if slug and not SLUG_RE.match(slug):
            errors.append("%s: slug %r is not kebab-case" % (where, slug))
        if slug in seen:
            errors.append("%s: slug %r duplicates %s" % (where, slug, seen[slug]))
        seen[slug] = where
        appears = unit_re.findall(f.get("appears", "")) if unit_re else []
        if unit_re and f.get("appears") and not appears:
            errors.append("%s: '%s' appears %r has no %s code matching %r" % (
                where, e["_name"], f["appears"], cfg["units"].get("name") or "unit", pattern))
        if is_moment and e["_unit"] and e["_unit"] not in appears:
            appears = [e["_unit"]] + appears
        if is_moment and unit_re and not e["_unit"]:
            errors.append("%s: moment '%s' sits under a heading with no unit code" % (where, e["_name"]))
        text = " ".join(f.values()).lower()
        quotes = re.findall(r"[\"“](.+?)[\"”]", f.get("quotes", "")) or ([f["quotes"]] if f.get("quotes") else [])
        rows.append({
            "slug": slug,
            "name": e["_name"],
            "kind": e["_kind"],
            "section": e["_section"],
            "tier": tier,
            "what": f.get("what", ""),
            "maps_to": f.get("maps-to", ""),
            "visual": f.get("visual", ""),
            "lighting": f.get("lighting", ""),
            "appears": appears,
            "aliases": split_list(f.get("aliases", "")),
            "quotes": quotes,
            "source": f.get("source", ""),
            "who": split_list(f.get("who", "")),
            "where": f.get("where", ""),
            "tone": split_list(f.get("tone", "")),
            "follows": f.get("follows", ""),
            "weight": f.get("weight", ""),
            "refs": {"folders": [], "pointers": split_list(f.get("refs", ""))},
            "unverified": "(unverified)" in text,
            "proposed": "(proposed)" in text,
            "file": e["_file"],
            "line": e["_line"],
            "_unit": e["_unit"],
        })

    by_slug = {r["slug"]: r for r in rows if r["slug"]}
    alias_owner = {}
    for r in rows:
        for a in r["aliases"]:
            sa = slugify(a)
            if sa in by_slug and sa != r["slug"]:
                errors.append("%s:%d: alias %r of '%s' is the slug of another entry; merge them" % (r["file"], r["line"], a, r["name"]))
            if sa in alias_owner and alias_owner[sa] != r["slug"]:
                warnings.append("alias %r is on both %s and %s" % (a, alias_owner[sa], r["slug"]))
            alias_owner[sa] = r["slug"]

    # ---- moments: who, where, follows, tone, weight ----
    outline_set = set(outline)
    for r in rows:
        where = "%s:%d" % (r["file"], r["line"])
        for code in r["appears"]:
            if outline and code not in outline_set:
                warnings.append("%s: '%s' appears in %s, which is not in 01" % (where, r["name"], code))
        if r["kind"] != "moment":
            continue
        for s in r["who"]:
            if s not in by_slug or by_slug[s]["kind"] == "moment":
                errors.append("%s: moment '%s' has who %r, which is not a character or thing slug" % (where, r["name"], s))
        w = r["where"]
        if w and SLUG_RE.match(w) and "-" in w and w not in by_slug:
            warnings.append("%s: moment '%s' has where %r: it looks like a slug but no entry has it" % (where, r["name"], w))
        if r["follows"]:
            prev = by_slug.get(r["follows"])
            if not prev or prev["kind"] != "moment":
                errors.append("%s: moment '%s' follows %r, which is not a moment slug" % (where, r["name"], r["follows"]))
            elif prev["_unit"] != r["_unit"]:
                warnings.append("%s: moment '%s' follows %r from another unit" % (where, r["name"], r["follows"]))
        for t in r["tone"]:
            if tones and t not in tones:
                errors.append("%s: moment '%s' has tone %r, not in [moments] tones" % (where, r["name"], t))
        if r["weight"] and r["weight"] not in ("major", "minor"):
            errors.append("%s: moment '%s' has weight %r, expected major or minor" % (where, r["name"], r["weight"]))

    # ---- story_weight: how many moments each thing drives ----
    drives = {}
    for r in rows:
        if r["kind"] == "moment":
            for s in set(r["who"] + ([r["where"]] if r["where"] in by_slug else [])):
                drives[s] = drives.get(s, 0) + 1
    for r in rows:
        if r["kind"] != "moment":
            n = drives.get(r["slug"], 0)
            r["drives_moments"] = n
            r["story_weight"] = "major" if n >= 3 else "minor" if n else "none"

    # ---- refs: refs/<category>/<slug, alias or name>/ ----
    refs_root = os.path.join(root, "refs")
    cats = sorted(d for d in os.listdir(refs_root) if os.path.isdir(os.path.join(refs_root, d))) if os.path.isdir(refs_root) else []
    matched = set()
    for r in rows:
        cands = list(dict.fromkeys([r["slug"], slugify(r["name"])] + [slugify(a) for a in r["aliases"]]))
        for c in cands:
            for cat in cats:
                d = os.path.join(refs_root, cat, c)
                if c and os.path.isdir(d):
                    matched.add((cat, c))
                    for p in list_images(d):
                        rp = os.path.relpath(p, root).replace(os.sep, "/")
                        if rp not in r["refs"]["folders"]:
                            r["refs"]["folders"].append(rp)
        r["ref_count"] = len(r["refs"]["folders"]) + len(r["refs"]["pointers"])
        r["gap"] = bool(visual and cats and r["kind"] != "moment" and r["tier"] in top_tiers and r["ref_count"] < gap_min)
    orphans = ["%s/%s" % (cat, d) for cat in cats for d in sorted(os.listdir(os.path.join(refs_root, cat)))
               if os.path.isdir(os.path.join(refs_root, cat, d)) and (cat, d) not in matched]

    for r in rows:
        del r["_unit"]
    with open(os.path.join(root, "index.json"), "w", encoding="utf-8") as fh:
        json.dump(rows, fh, indent=1, ensure_ascii=False)
        fh.write("\n")

    # ---- stats ----
    things = [r for r in rows if r["kind"] != "moment"]
    moments = [r for r in rows if r["kind"] == "moment"]
    kinds = sorted({r["kind"] for r in rows if r["kind"]})
    order = lambda r: (tiers.index(r["tier"]) if r["tier"] in tiers else 9, r["slug"])
    units_with_moments = {r["appears"][0] for r in moments if r["appears"]}
    bare_units = [u for u in outline if u not in units_with_moments]
    unmoved = [r for r in things if r["tier"] in top_tiers and r["drives_moments"] == 0] if moments else []
    gaps = sorted((r for r in rows if r["gap"]), key=order)

    out = ["project: %s (%s mode, feeds %s)" % (project.get("name") or "unnamed", project["mode"], project.get("target") or "?"),
           "entries: %d (things %d, moments %d)" % (len(rows), len(things), len(moments)),
           "%s in 01: %d, without moments: %d" % (cfg.get("units", {}).get("name") or "units", len(outline), len(bare_units)),
           "unverified: %d, proposed: %d" % (sum(r["unverified"] for r in rows), sum(r["proposed"] for r in rows)),
           "SHORT voice lines: %d" % flagged,
           "errors: %d, warnings: %d" % (len(errors), len(warnings)),
           "",
           "kind x tier:"]
    for k in kinds:
        out.append("  %-12s %s" % (k, "  ".join("%s=%d" % (t, sum(1 for r in rows if r["kind"] == k and r["tier"] == t)) for t in tiers)))
    out.append("story weight (things): " + ", ".join("%s=%d" % (w, sum(1 for r in things if r["story_weight"] == w)) for w in ("major", "minor", "none")))
    sizes = []
    for no, fn in sorted(files.items()):
        with open(os.path.join(root, "bible", fn), encoding="utf-8") as fh:
            n = sum(1 for _ in fh)
        sizes.append("  %-24s %d lines%s" % (fn, n, "  (over %d)" % FILE_MAX_LINES if n > FILE_MAX_LINES else ""))
    out += ["", "files:"] + sizes
    if errors:
        out += ["", "errors (%d):" % len(errors)] + ["  " + e for e in errors]
    if warnings:
        out += ["", "warnings (%d):" % len(warnings)] + ["  " + w for w in warnings]
    if bare_units:
        out += ["", "%s with no moments (%d):" % (cfg["units"].get("name") or "units", len(bare_units)), "  " + " ".join(bare_units)]
    if unmoved:
        out += ["", "%s entries that drive no moment (%d):" % (" and ".join(top_tiers), len(unmoved))]
        out += ["  %-9s %-10s %s" % (r["tier"], r["kind"], r["slug"]) for r in sorted(unmoved, key=order)]
    if cats:
        out += ["", "gaps: %s entries with under %d reference images (%d):" % (" and ".join(top_tiers), gap_min, len(gaps))]
        out += ["  %-9s %-10s %-32s %d" % (r["tier"], r["kind"], r["slug"], r["ref_count"]) for r in gaps]
        out += ["", "folders in refs/ with no entry (%d):" % len(orphans)] + ["  " + o for o in orphans]
    with open(os.path.join(root, "index-stats.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")

    print("\n".join(out[:6]))
    if errors:
        print("\n".join("  " + e for e in errors[:15]))
        print("%d errors, all in index-stats.txt" % len(errors))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
