#!/usr/bin/env python3
"""Check lore pass files against the index.

  python3 -I tools/check_pass.py [passes/batch.md ...] [--root DIR]

With no files, checks every passes/*.md. Errors: a missing field, a slug the index does not
have, a carrier used twice across all passes, a flavor line over [voice] line_max.
Stdlib only, Python 3.11+. Needs index.json (run build_index.py first). Exits 1 on any error.
"""
import argparse
import glob
import json
import os
import re
import sys
import tomllib

FIELDS = ["does", "idea", "carrier", "because", "name", "scene", "flavor", "alt", "cites"]


def parse(path):
    items, cur = [], None
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            if line.startswith("### "):
                cur = {"_name": line[4:].strip(), "_file": path, "_line": n, "_f": {}}
                items.append(cur)
                continue
            m = re.match(r"^- ([a-z]+): ?(.*)$", line.rstrip("\n"))
            if cur is not None and m:
                cur["_f"][m.group(1)] = m.group(2).strip()
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    index_path = os.path.join(root, "index.json")
    if not os.path.isfile(index_path):
        sys.exit("no index.json in %s: run python3 -I tools/build_index.py first" % root)
    slugs = set()
    for r in json.load(open(index_path, encoding="utf-8")):
        slugs.add(r["slug"])
    with open(os.path.join(root, "lore.toml"), "rb") as fh:
        line_max = tomllib.load(fh).get("voice", {}).get("line_max", 90)

    every = sorted(glob.glob(os.path.join(root, "passes", "*.md")))
    targets = [os.path.abspath(f) for f in a.files] or every
    carriers = {}
    for path in sorted(set(every) | set(targets)):
        for it in parse(path):
            c = it["_f"].get("carrier", "")
            if c:
                carriers.setdefault(c, []).append((path, it["_line"]))

    errors, count = [], 0
    for path in targets:
        for it in parse(path):
            count += 1
            f = it["_f"]
            where = "%s:%d '%s'" % (os.path.relpath(path, root), it["_line"], it["_name"])
            for k in FIELDS:
                if not f.get(k):
                    errors.append("%s: missing '%s'" % (where, k))
            c = f.get("carrier", "")
            if c and c not in slugs:
                errors.append("%s: carrier %r is not in the index" % (where, c))
            others = [x for x in carriers.get(c, []) if x != (path, it["_line"])]
            if c and others:
                errors.append("%s: carrier %r also carries %s" % (
                    where, c, ", ".join("%s:%d" % (os.path.relpath(p, root), n) for p, n in others)))
            used = [x.strip().strip("`") for x in f.get("cites", "").split(",")]
            used += [part.split(",")[0].strip().strip("`") for part in f.get("alt", "").split(";")]
            used += re.findall(r"`([a-z0-9-]+)`", f.get("scene", ""))
            for s in used:
                if s and s not in slugs:
                    errors.append("%s: slug %r is not in the index" % (where, s))
            m = re.search(r"[\"“](.+?)[\"”]", f.get("flavor", ""))
            line = m.group(1) if m else f.get("flavor", "")
            if len(line) > line_max:
                errors.append("%s: flavor is %d characters, the limit is %d" % (where, len(line), line_max))

    print("%d items in %d file(s), %d errors" % (count, len(targets), len(errors)))
    for e in errors:
        print("  " + e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
