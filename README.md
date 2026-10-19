# Lore builder

A kit for building a lore bible for any world: a show you're adapting, a game you're designing, a novel, a tabletop campaign. You get a fixed file layout, an entry format, four agent skills that do the work with you, and three small Python tools that turn the bible into a searchable index and check it for mistakes.

It grew out of the Rick and Morty bible in Proxy Magic, which mapped a whole TV show onto Magic cards. Everything specific to that show and to Magic has been taken out. What's left is the method.

## The idea

**The bible is an index, not an encyclopedia.** Every character, place, thing and story beat is a short lookup row: what it is, what it could be used for in your project (`maps-to`), how well the audience knows it (`tier`), and where its pictures are. Nobody reads the bible end to end. People and agents search it, find the three entries they need, and go.

Three things make that work:

- **One slug per thing.** `the-brinewarden`, never two entries for the same character. Other names are aliases.
- **Moments, not just nouns.** Beats from the story (a betrayal, a cure that backfires, a raid) are entries too, with a tone, a weight, and a link to the beat they follow. Chains of moments are things that belong together.
- **Three separate axes.** `tier` is fame with the audience. `story_weight` is how much a thing drives the plot (the tools work it out). `(unverified)` and `(proposed)` mark how sure you are. Mixing them up is how bibles go wrong.

## Quick start

1. Copy this whole folder and rename it for your world.
2. Open it in Claude Code and run `/lore-setup`. It interviews you: adaptation or original world, what the bible feeds (cards, quests, levels, chapters), what your story units are (episodes, chapters, quests), and which sources you trust. It writes `lore.toml`.
3. Add lore: "add the main cast", "build moments for season 1", or paste your notes. That's `/lore-build`.
4. Use it: "theme these 20 quests" or "find lore for this decklist". That's `/lore-pass`.
5. Check it now and then: `/lore-check`.

Not using Claude Code? `AGENTS.md` is read by most coding agents (Codex, Cursor, Copilot and others), and each skill is a plain markdown file in `.claude/skills/<name>/SKILL.md` any agent or person can follow.

## Two modes

- **Adaptation**: an existing work. Facts come from sources, every entry cites one, and nothing gets invented. Thin facts are marked `(unverified)`.
- **Original**: your own world. Facts come from you. An agent can fill gaps, but anything it invents is marked `(proposed)` until you approve it, and your approvals go in `DECISIONS.md` so entries can cite them.

## What's in the folder

```
lore.toml        fits the kit to your project: mode, target, units, tiers, tones
FORMAT.md        the entry format and the rules (the one place they're written)
AGENTS.md        what an agent reads first; CLAUDE.md points to it
DECISIONS.md     numbered calls you've made about your world
bible/
  00 index.md    how to use the bible, the mapping rubric, the voice guide, the tier rule
  01 outline.md  every episode, chapter or quest, one line each
  02 characters.md
  03 places.md   locations, realms, factions, events
  04 things.md   items, weapons, vehicles, substances, media
  05 style.md    the look, for artists and image models
  06 voice.md    quotes and catchphrases by speaker
  07 sources.md  the sources you trust and what each covers
  08 moments.md  two to six story beats per unit
  09 ideas.md    products, arcs or campaigns the bible suggests
passes/          lore passes: your project's items translated into the world
refs/            reference images, one folder per slug (kept out of git)
tools/           build_index.py, search.py, check_pass.py
examples/salt-archive/   a small finished bible to look at
```

## Commands

Python 3.11 or newer, nothing to install.

```bash
python3 -I tools/build_index.py
```

Builds `index.json` and `index-stats.txt` and checks everything: the format, duplicate slugs, broken links between moments and characters, tones outside your list, quotes over your length limit, units with no moments, and important entries with too few reference images. Exits with an error code if anything's broken.

```bash
python3 -I tools/search.py "a cure that makes things worse"
```

Keyword search over the index. Also `--slug <slug>` for one entry in full, `--who <slug>` for every moment a character drives, `--unit <code>` for everything in one episode or chapter, and `--kind` and `--tier` filters.

```bash
python3 -I tools/check_pass.py
```

Checks the files in `passes/`: every field filled, every slug real, no carrier used twice.

Every tool takes `--root <folder>` to work on a bible somewhere else. Try them on the example:

```bash
python3 -I tools/search.py "something that stops everyone" --root examples/salt-archive
```

## Reference images

Drop pictures in `refs/<anything>/<slug>/` (for example `refs/characters/the-brinewarden/1.jpg`). The index links them to the entry by slug, alias or name, and lists famous entries that have fewer than three. `.gitignore` keeps them out of git, since they're usually someone else's art.

## Going further

The Proxy Magic bible had heavier tooling on top of this core, worth rebuilding if your project needs it: a vision model that tags every reference image with the bible's slugs, semantic search with local embeddings, fame scores from public signals (video views, wiki links) to set `tier` from evidence, and a checker that compares moments against each episode's plot text to find beats that were missed.
