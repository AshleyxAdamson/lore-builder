#!/usr/bin/env python3
"""Search the bible index (index.json) by words, slug or character.

  python3 -I tools/search.py "a cure that makes things worse" [--kind moment] [--tier iconic,known] [--n 10]
  python3 -I tools/search.py --slug some-slug        # one entry in full
  python3 -I tools/search.py --who some-slug         # the moments a character, thing or place drives
  python3 -I tools/search.py --unit S1E6             # every entry in one unit, moments in order

Add --root DIR when the lore folder is not the one above tools/. Stdlib only.
Scoring is keyword overlap weighted by field (name and aliases first, then maps-to, what, visual).
It finds words, not ideas: search the idea in two or three phrasings.
"""
import argparse
import json
import os
import re
import sys
import tomllib

FIELDS = [("name", 5), ("aliases", 5), ("slug", 4), ("maps_to", 3), ("what", 2), ("tone", 2),
          ("visual", 1), ("quotes", 1), ("section", 1), ("who", 1), ("where", 1)]
STOP = set("a an the of to in on and or for with that this is it its by as at from be are was who what".split())


def words(s):
    out = []
    for w in re.findall(r"[a-z0-9]+", s.lower()):
        if len(w) > 1 and w not in STOP:
            out.append(w[:-1] if len(w) > 4 and w.endswith("s") else w)
    return out


def field_text(r, f):
    v = r.get(f, "")
    return " ".join(v) if isinstance(v, list) else str(v)


def score(r, q_words, q_phrase):
    s = 0.0
    for f, w in FIELDS:
        text = field_text(r, f)
        have = set(words(text))
        s += w * sum(1 for q in q_words if q in have)
        if q_phrase and q_phrase in text.lower():
            s += 2 * w
    return s


def show(r, full=False):
    head = "%s  [%s, %s]  %s" % (r["slug"], r["kind"], r["tier"], r["name"])
    if r.get("story_weight") and r["story_weight"] != "none":
        head += "  story:%s" % r["story_weight"]
    flags = [x for x in ("unverified", "proposed") if r.get(x)]
    if flags:
        head += "  (" + ", ".join(flags) + ")"
    lines = [head, "    " + r["what"], "    maps-to: " + r["maps_to"]]
    if r["kind"] == "moment":
        lines.append("    who: %s · where: %s · tone: %s · follows: %s · weight: %s" % (
            ", ".join(r["who"]), r["where"], ", ".join(r["tone"]), r["follows"] or "-", r["weight"]))
    if full:
        for k in ("aliases", "appears", "visual", "lighting", "quotes", "source", "ref_count", "file", "line"):
            if r.get(k) not in (None, "", []):
                lines.append("    %s: %s" % (k, ", ".join(r[k]) if isinstance(r[k], list) else r[k]))
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="?", default="")
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--slug")
    ap.add_argument("--who")
    ap.add_argument("--unit")
    ap.add_argument("--kind", help="comma separated kinds")
    ap.add_argument("--tier", help="comma separated tiers")
    ap.add_argument("--n", type=int, default=10)
    a = ap.parse_args()
    path = os.path.join(a.root, "index.json")
    if not os.path.isfile(path):
        sys.exit("no index.json in %s: run python3 -I tools/build_index.py first" % a.root)
    rows = json.load(open(path, encoding="utf-8"))
    kinds = set(a.kind.split(",")) if a.kind else None
    tiers = set(a.tier.split(",")) if a.tier else None
    rows = [r for r in rows if (not kinds or r["kind"] in kinds) and (not tiers or r["tier"] in tiers)]

    if a.slug:
        hit = [r for r in rows if r["slug"] == a.slug or a.slug in r["aliases"]]
        print("\n\n".join(show(r, full=True) for r in hit) or "no entry %r" % a.slug)
        return 0
    if a.who:
        hit = [r for r in rows if r["kind"] == "moment" and (a.who in r["who"] or r["where"] == a.who)]
        print("%d moments\n" % len(hit) + "\n\n".join(show(r) for r in hit))
        return 0
    if a.unit:
        hit = [r for r in rows if a.unit in r["appears"]]
        hit.sort(key=lambda r: (r["kind"] == "moment", r["file"], r["line"]))
        print("%d entries\n" % len(hit) + "\n\n".join(show(r) for r in hit))
        return 0
    if not a.query:
        ap.error("give a query, --slug, --who or --unit")
    q_words, q_phrase = words(a.query), a.query.lower().strip()
    with open(os.path.join(a.root, "lore.toml"), "rb") as fh:
        tier_list = tomllib.load(fh).get("tiers", {}).get("values", [])
    tier_rank = {t: i for i, t in enumerate(tier_list)}
    scored = [(score(r, q_words, q_phrase), r) for r in rows]
    scored = [x for x in scored if x[0] > 0]
    scored.sort(key=lambda x: (-x[0], tier_rank.get(x[1]["tier"], 9), x[1]["slug"]))
    print("\n\n".join(show(r) for _, r in scored[:a.n]) or "nothing matched; try other words")
    return 0


if __name__ == "__main__":
    sys.exit(main())
