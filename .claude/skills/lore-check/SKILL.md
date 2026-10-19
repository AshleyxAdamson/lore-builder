---
name: lore-check
description: Audit the lore bible for parse errors, contradictions, coverage gaps and drift from the format. Use when the owner asks whether the bible is consistent or complete, after a big build pass, or before a lore pass leans on it.
---

# Lore check

Two layers. The **mechanical** layer is what `tools/build_index.py` already catches: format, slugs, tiers, tones, broken `who` and `follows` links, SHORT lines over the limit, coverage counts. The **reading** layer is what only a reader catches: two entries that say different things about the same fact. Run both; the report lists what you fixed and what needs the owner.

## Steps

1. **Build.** `python3 -I tools/build_index.py`, then read all of `index-stats.txt`.
2. **Fix every error** in the markdown, rebuild, repeat until zero. These are format slips, so fix them without asking, except a duplicate slug: merging two entries is a canon call when their facts differ.
3. **Triage the warnings and lists** in `index-stats.txt`: units with no moments, iconic and known entries that drive no moment, gaps in reference images, orphan `refs/` folders, files over the line budget. Each becomes a fix you make now, or a line in the report.
4. **Read for contradictions**, one file pair at a time, with the index open: a character's `what` against the moments they appear in (`tools/search.py --who <slug>`); `appears` against `01`; a place's `lighting` against `05 style.md`; quotes in entries against `06`; slugs named in `00` and `09` against the index. Hunt for one fact told two ways: an age, a relation, an allegiance, an order of events, a color.
5. **Read for drift** from `FORMAT.md`: `visual` lines over 15 words or with praise words, `maps-to` lines with no reason, `tier` set from one unit's importance rather than from the audience, prose creeping into what should be a lookup row.
6. **Report** in four short lists: fixed (with counts), contradictions (each with both sources and the files and lines), owner questions (canon calls, merges, tiers), and the next `lore-build` targets (largest coverage gaps first).

Done when the build has zero errors and every warning and contradiction is either fixed or in the report. In original mode, a contradiction between two owner facts is never resolved by you: it goes to the owner, and their answer becomes a decision in `DECISIONS.md`.
