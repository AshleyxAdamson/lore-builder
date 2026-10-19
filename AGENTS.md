# Lore bible

This folder is a lore bible: a searchable index of one world (characters, places, things, moments) that feeds the target named in `lore.toml`. `README.md` explains it for people.

- **Before writing in `bible/`**, read `FORMAT.md`. It is the entry shape and the rules.
- **Search, don't read.** `python3 -I tools/search.py "<words>"` (also `--slug`, `--who`, `--unit`). Open a bible file only for the entry you need.
- **After every edit**, `python3 -I tools/build_index.py`. Zero errors is the bar; `index-stats.txt` holds the rest.
- **Canon calls** the owner settles go in `DECISIONS.md` as the next number, with the reason.
- `index.json` and `index-stats.txt` are generated. `refs/` holds images and stays out of git.

## Skills

Each is a folder in `.claude/skills/` with a `SKILL.md`. Agents without skill support read that file and follow it.

- `lore-setup`: fit the kit to a project (run first, when `lore.toml` has an empty mode).
- `lore-build`: add entries and moments, run a first pass over a whole work, refresh `00 index.md`.
- `lore-pass`: translate target items (cards, quests, levels) into the world, one carrier each.
- `lore-check`: audit for errors, contradictions, gaps and drift.
