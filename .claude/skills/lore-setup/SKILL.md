---
name: lore-setup
description: Start a new lore bible, or refit this kit to a different project. Use when lore.toml has an empty mode, or the owner wants to change the target, unit, tiers or tone vocabulary.
---

# Lore setup

Fits the kit to one project by interviewing the **owner** (the person whose world or product this is) and writing their answers into `lore.toml`, `bible/00 index.md` and `DECISIONS.md`. Everything the other skills do reads from these three files, so a vague answer here becomes a vague bible later. `FORMAT.md` is the entry shape; read it first.

## Steps

1. **Interview.** Ask these in small batches, offering a concrete default for each so the owner can answer "yes":
   - What is the world, in two sentences? Is it an existing work you are adapting (a show, book, game, film) or a world you are inventing? This sets `mode`.
   - What will the bible feed? Cards, quests, levels, enemies, chapters, a pitch deck, merchandise. This is the `target`, and it names the `maps-to` vocabulary.
   - What is the unit the story is told in? Episode, chapter, quest, level, session. What does a unit code look like? This sets `[units]`. An invented world with no story yet may leave the pattern empty.
   - Will artists or an image model work from the bible? This sets `visual`.
   - Who is the audience whose fame `tier` measures? For an adaptation it is the work's audience. For an original world it is the people who will play or read it, and `tier` says how central a thing is meant to be to them.
   - Which tones does the world run on? Start from the list in `lore.toml`, cut what never fits, add what is missing.
   - For an adaptation: which sources are trusted, in order (official site, scripts, art books, a fan wiki, Wikipedia)? For an original world: which existing documents hold canon (a design doc, a pitch, notes)?
2. **Write `lore.toml`.** Fill every field from the answers. Test the unit pattern against two real codes with `python3 -c 'import re; print(re.findall(r"<pattern>", "<codes>"))'`.
3. **Write the skeleton of `bible/00 index.md`.** Fill the sections the answers already settle: section 2's table header names the target ("<target> idea | Lore that carries it | Slugs"), with a starter list of eight to fifteen target ideas in the first column and the other columns empty; section 4's tier rule written for this audience; the tone table with each kept tone mapped to an axis of the target (colors, factions, moods, difficulty), or a note that the owner will choose the axis later. Leave the rest as the template has it: the synthesis step of `lore-build` fills it once entries exist.
4. **Write `bible/07 sources.md`.** List the trusted sources in the owner's order, with what each one is good for.
5. **Record the setup in `DECISIONS.md`** as decision 1: mode, target, unit, audience, and why, in the owner's words.
6. **Build.** `python3 -I tools/build_index.py` runs with zero errors on the empty bible.

Done when `lore.toml` has no empty field the owner could answer, the build has zero errors, and decision 1 is written. Then offer `lore-build` as the next step.

## Refitting an existing bible

When the owner changes the target or the unit on a bible that already has entries, the old `maps-to` lines and unit codes go stale. Write the change as a new decision, then list in that decision how many entries the change touches (`python3 -I tools/search.py` and `index-stats.txt` count them) and ask whether to rewrite `maps-to` now or as entries are next touched.
