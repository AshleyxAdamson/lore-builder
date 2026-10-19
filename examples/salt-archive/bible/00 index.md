# 00 Index: how to use the bible, the mapping rubric, the voice guide

This folder is a lookup system. Search the index; open a prose file only for the entry you need.

## 1. How to use the bible

- Search: `python3 -I tools/search.py "<words>" --root examples/salt-archive`, or `--slug`, `--who`, `--unit`.
- Rebuild after every edit: `python3 -I tools/build_index.py --root examples/salt-archive`.
- The one rule of magic is DECISIONS 2. Anything that bends it is out.

## 2. Mapping rubric: quest and item ideas to lore

| Target idea | Lore that carries it | Slugs (iconic > known > deep-cut) |
|---|---|---|
| Fetch quest | Recovering a lost memory | `memory-lamp`, `q1-wren-tastes-a-memory`; known `low-tide-market` |
| Healing item | Salt that carries a calm memory | `white-salt` |
| Stealth section | The sealed stacks, the smugglers' routes | `the-salt-archive`, `the-undertow` |
| Boss fight | Someone guarding grief | `the-brinewarden`; known `q3-undertow-raid` |
| Vehicle or fast travel | Boats on the drowned streets | known `tidecaller-skiff` |
| Weapon | No clean carrier; the world has few weapons. Nearest: the smugglers' tool | known `brine-knife` |

## 3. Voice guide

- Wren: curious, quick, asks questions instead of stating. "What did it taste like to you?"
- The Brinewarden: slow, kind, final. Never raises her voice.
- Tamsin: prices everything, jokes about the dead.
- Narrator register: second person, present tense, one sensory detail, no exclamation marks.

## 4. Tier rule

- `iconic`: every player meets it in the first hour and remembers it.
- `known`: a player who finishes the main quests meets it.
- `deep-cut`: found only by exploring.

## Tone to target

| Tone | Maps to | Why |
|---|---|---|
| tender, mournful | healing and support items | memories of the dead as comfort |
| clever, greedy | trade and stealth quests | the Undertow and the market |
| orderly, cold | boss fights and locked areas | the Archive's seals |
