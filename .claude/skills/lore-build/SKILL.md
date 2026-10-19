---
name: lore-build
description: Add to or grow the lore bible: new characters, places, things, moments for a unit, or a whole first pass over a work. Use when the owner names something to add, pastes notes or a source to turn into entries, or asks to fill a season, chapter or category.
---

# Lore build

Writes entries into `bible/` in the shape `FORMAT.md` sets, then rebuilds the index. Read `FORMAT.md` and `lore.toml` first. Then read the file for this project's mode, which says where facts come from and what counts as a source:

- `mode = "adaptation"`: [`adaptation.md`](adaptation.md)
- `mode = "original"`: [`original.md`](original.md)

## Steps for any addition

1. **Search before writing.** `python3 -I tools/search.py "<name and two other phrasings>"`. A hit on the same thing under another name becomes an alias on the existing entry, and the facts go there. One canonical slug per thing.
2. **Get the lore right.** Fill `what`, `appears`, `source` and `visual` from the sources the mode file names. A field that rests on one thin source carries `(unverified)`; a field you invented carries `(proposed)`.
3. **Then map it.** `maps-to` names two to four ideas from the target, each with a few words why. Use the words already in section 2 of `00 index.md` when one fits, so the index stays searchable.
4. **Set the tier** by the tier rule in `00 index.md`. Without evidence about the audience, use `known` and say so in the report.
5. **Rebuild.** `python3 -I tools/build_index.py` and fix every error in the markdown.

Done when the build has zero errors and every new slug shows up in `python3 -I tools/search.py --slug <slug>`.

## Moments for a unit

1. Read the unit's source (plot summary, script, chapter, quest design) and list its beats.
2. Write two to six moments under the unit's `## <code> · <title>` heading in `08`, in story order. Pick beats a target item could be named after: reversals, cures that backfire, betrayals, heists, sacrifices, resets. Actions and events are moments; nouns are things and go in 02 to 04.
3. Give each its `who` (slugs, adding missing characters to 02 first), `where`, `tone` from the vocabulary, `weight`, and `follows` when it is the consequence of an earlier beat in the same unit.
4. Rebuild. Read `index-stats.txt`: the unit leaves the "with no moments" list, and every iconic or known entry the unit introduces drives at least one moment, or you note why it does not.

## A whole work or a big category

Split by **sequence**: one reader per block of units (a season, an act, ten chapters), each a subagent with `FORMAT.md`, `lore.toml`, the mode file and its block's sources, writing to a scratch file of entries rather than to `bible/`. Then merge: dedupe slugs across readers, turn duplicates into aliases, write into `bible/`, rebuild. A reader on a block it knows well from training still checks each beat against the source text; a reader on recent or obscure material works from the source text alone.

Order the passes: 01 outline first (every unit, one line), then 02 to 04 (things), then 08 (moments, which need the thing slugs), then 06 voice, then synthesis.

## Synthesis

After a pass that added more than a handful of entries, refresh `bible/00 index.md`:

- Section 2, the mapping rubric: for each target idea, the lore that carries it and its slugs, iconic first. Where the bible has no clean carrier, the row says so and names the nearest one.
- Section 3, the voice guide: how each main speaker talks, drawn from `06`, with one example line each, and the narrator register for text that no character speaks.
- The cross-cutting themes table: ideas that recur across units and deserve their own search terms.
- `09 ideas.md`: the products, arcs or decks the bible now throws off, each with its slugs and moments.

Every slug named in 00 and 09 exists in the index (`tools/search.py --slug`).
