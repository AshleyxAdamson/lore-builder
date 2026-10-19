---
name: lore-pass
description: Translate a batch of target items (cards, quests, levels, enemies, chapters) into the world by finding the lore that carries each one. Use when the owner has a list of things to theme, rename or dress with the bible.
---

# Lore pass

A lore pass takes **items** of the target (a decklist, a quest list, a level plan) and finds, for each, the lore that carries the same idea: its **carrier**. It writes one file, `passes/<batch>.md`, and `tools/check_pass.py` checks it. Read `lore.toml` and sections 2 to 4 of `bible/00 index.md` (the rubric, the voice guide, the tier rule) before the first item.

## Entry shape

```
### <item as the target knows it>
- does: what the item does in the target, in the target's own terms
- idea: the target idea it expresses, in the rubric's words
- carrier: the slug whose lore carries that idea
- because: one sentence on why this carrier fits the idea
- name: the item's name in the world
- scene: the characters, place and props as `slugs` in backticks, then one visible event
- flavor: one line in the voice guide's rules, within line_max
- alt: slug, reason; slug, reason
- cites: every slug this entry drew on
```

## Steps

1. **Rank the items** by importance in the target (the headline item first, filler last). Tier follows importance: iconic carriers go on headline items, deep cuts on filler, where they reward close fans.
2. **Reuse first.** Search earlier files in `passes/` for each item. An item already translated keeps its name, carrier and scene unless the owner asks for a new one.
3. **Find the carrier by search**, never from memory: look the item's idea up in the rubric, then search the bible for the idea in two or three phrasings (`python3 -I tools/search.py "<idea>"`, `--kind moment` for actions, `--who <slug>` for a character's beats). Carriers are moments and themes as often as characters: an action item (a spell, an ambush, a twist) usually wants a moment. A chain of moments (`follows`) is a set of items that want to be used together.
4. **Keep carriers unique.** A carrier slug carries one item across all passes. A character may still appear in many scenes, and may carry several items when each is a different state or version of them with its own slug.
5. **Write the entry**, with two alternates and a reason for each, so the owner can swap without a new search.
6. **Check.** `python3 -I tools/check_pass.py passes/<batch>.md`.

Done when every item has an entry and the check reports zero errors. Report the items whose best carrier was weak (no rubric row fit, or the carrier is `(unverified)` or `(proposed)`): those are where the bible needs a `lore-build` pass.
