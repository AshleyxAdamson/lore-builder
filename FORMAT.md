# Bible format (read before writing any file in `bible/`)

The bible is an **index, not an encyclopedia**. Every entry is a lookup row: what the thing is, what it can be used for (`maps-to`), how well the audience knows it (`tier`), and where its pictures are (`refs`). Long prose descriptions are out: a reader, an artist or an image model gets detail from sources and reference images, and the text only has to find them. `tools/build_index.py` flattens the entries into `index.json`; agents search that file and open a bible file only for the entry they need.

`lore.toml` fits this format to a project: the mode, the target, the unit, the tiers, the tone vocabulary and the kinds. Words in angle brackets below (`<target>`, `<unit>`) come from there.

## Files

All in `bible/`. Numbers and roles are fixed; the words after the number may change (`04 tech.md` is fine).

```
00 index.md      how to use the bible, the mapping rubric, the voice guide, the tier rule, cross-cutting themes, tone table (written last)
01 outline.md    every <unit> in order, one line each
02 characters.md named characters, their variants, species and creature types
03 places.md     locations, realms, factions and organizations, events
04 things.md     items, devices, weapons, vehicles, substances, media inside the world
05 style.md      the look: line, palette, lighting per setting, typography (skip when visual = false)
06 voice.md      quotes, catchphrases and running jokes, by speaker
07 sources.md    what each primary source covers: art books, design docs, scripts, wikis, with a page index
08 moments.md    two to six beats per <unit>: the things that happen
09 ideas.md      products, decks, arcs or campaigns the bible throws off
```

`index.json` and `index-stats.txt` sit beside `lore.toml` and are generated. Never edit them. `refs/` holds reference images, one folder per slug.

## Entry shape (02, 03, 04)

```
### <Name>
- slug: kebab-case, unique across the bible, never changed once used
- aliases: other names people use, comma separated (optional)
- what: one or two sentences, what it is in the world
- appears: <unit> codes, first appearance first (required when lore.toml sets a unit pattern)
- tier: iconic | known | deep-cut
- maps-to: the <target> ideas this fits, with a few words why
- visual: 8 to 15 words, only what a prompt needs to name it: shape, colors, clothing (required when visual = true)
- lighting: the light and palette of a place (optional, places)
- refs: pointers to pictures outside refs/, such as art-book pages `v1-p42` (optional)
- quotes: up to three short lines tied to it (optional)
- source: a url, a document and page, or `owner` / `DECISIONS 12` in original mode
```

One `key: value` line per field, no blank lines inside an entry, no other text. A `#` or `##` heading above the entries sets their kind (see `[kinds]` in `lore.toml`). The parser rejects anything else, and the fix is always the markdown, never the parser.

## 01 outline

One line per <unit>, in order, under `##` headings for seasons, acts or books:

```
S1E1 · Pilot · one-line summary · introduces: Name, Name, Name
```

## 08 moments

Beats that a <target> item could be named after: a betrayal, a cure that backfires, a heist, a reset, a sacrifice. Actions, events and reversals map to moments; nouns map to things. Group them under a `## <code> · <title>` heading per <unit>. Same shape as above, plus:

```
- who: slugs of the characters, factions and things that act in it
- where: a place slug, or plain text when the place has no entry
- tone: two or three words from the tone vocabulary in lore.toml
- follows: the slug of the moment this one is the consequence of, in the same <unit> (empty for the first beat)
- weight: major | minor   (major: the <unit> turns on it; minor: a gag or an aside)
```

A moment's `appears` may be left out: it takes the <unit> from its heading. `follows` turns beats into **chains**: a chain is a package of <target> items that want to be used together. The index gives every thing a `story_weight` (major, minor, none) from how many moments it drives. That is a separate axis from `tier`.

## 06 voice

Under one `##` heading per speaker, one quote per line:

```
- "Exact line." · S1E1 · SHORT
```

Flag a line `SHORT` when it fits the `line_max` in lore.toml; the build checks every flagged line.

## The three axes

- **tier** is fame with the audience and nothing else: `iconic` (a casual audience member knows it), `known` (a fan knows it), `deep-cut` (one <unit>, a reward for close readers). Set it from evidence about the audience (views, mentions, a poll of real people), never from how big a thing feels in one <unit>.
- **story_weight** is how much a thing drives the plot. The index derives it from moments.
- **unverified / proposed** is confidence. Write `(unverified)` in a field that rests on one thin source; write `(proposed)` in a field an agent invented that the owner has not approved. The index flags both.

## Rules

- Lore first, mapping second: get `what` right before `maps-to`.
- Every entry has a `source`. In adaptation mode it points at the work or a source about it; in original mode it points at the owner's word (`owner`) or a numbered decision (`DECISIONS 12`).
- In adaptation mode, no speculation about unreleased material. In original mode, an agent's invention carries `(proposed)` until the owner approves it.
- One canonical slug per thing. A second name goes in `aliases`; duplicates are merged, never kept side by side.
- `visual` lines are for an artist or an image model: concrete nouns, colors, shapes, clothing. No praise words like "iconic" or "beautiful".
- Plain short sentences. No em dashes.
- Keep each file under about 700 lines. When a category outgrows that, keep the iconic and known tiers complete and sample the deep cuts.
- Rebuild after every edit: `python3 -I tools/build_index.py`. Zero errors is the bar.
