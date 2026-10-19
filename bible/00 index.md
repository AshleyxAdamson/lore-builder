# 00 Index: how to use the bible, the mapping rubric, the voice guide

This folder is a lookup system. Search the index; open a prose file only for the entry you need.

## 1. How to use the bible

- `index.json` has one row per entry in 02, 03, 04 and 08. Search it with `python3 -I tools/search.py "<words>"`, or `--slug`, `--who`, `--unit`.
- `index-stats.txt` has counts, errors, warnings, coverage gaps and reference gaps from the last build.
- `01` is one line per unit. `05` and `07` are the look and the sources. `06` is quotes and running jokes.
- Rebuild after every edit: `python3 -I tools/build_index.py`.
- Facts about the look: the primary sources in `07` win over `05`. Reference images beat any text line.
- Duplicates are merged. An alias on an entry points to the one canonical slug. Search aliases too.

## 2. Mapping rubric: target idea to lore

Slugs are listed iconic first, then known, then deep-cut. Every slug exists in the index. Where the bible has no clean carrier for an idea, the row says so and names the nearest one.

| Target idea | Lore that carries it | Slugs (iconic > known > deep-cut) |
|---|---|---|

## 3. Voice guide

Source: the lines in `06`. Lines flagged SHORT fit the `line_max` in `lore.toml`.

Hard limits:

- Within `line_max` characters. Plain short sentences. No em dashes.
- Original wording, or a line from `06` flagged SHORT.
- Attribute a line to a speaker the item's art or name can carry. Do not invent facts.

How each main speaker talks:

Narrator register (text no character speaks):

## 4. Tier rule

- `iconic`: 
- `known`: 
- `deep-cut`: 
- Spend iconic slugs on headline items and deep cuts on filler. Two items wanting the same iconic carrier share one translation.
- Entries flagged unverified or proposed in the index need a check before a headline item rests on them.

## Themes that cut across units

| Theme | What it is in the world | Target ideas it carries | Start here |
|---|---|---|---|

## Tone to target

Moments carry a `tone`. This table maps each tone to an axis of the target (colors, factions, moods, difficulty), so a product's identity reads off the moments it uses.

| Tone | Maps to | Why |
|---|---|---|
