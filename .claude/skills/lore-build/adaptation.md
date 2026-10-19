# Adaptation mode: facts come from the work

The bible describes a work that already exists. Every fact is checkable, and the job is to be right, not inventive.

## Sources

- Use the sources in `bible/07 sources.md`, in the owner's order. Typical order: the work itself (scripts, transcripts, the book text), official material (art books, the publisher's site), a fan wiki, Wikipedia.
- Fan wikis often block page scraping and allow their API. For MediaWiki sites (most fandom wikis): `https://<wiki>/api.php?action=parse&page=<Title>&prop=wikitext&format=json`. Fetch one page at a time and cache what you fetch.
- `source` is the url or document and page the `what` came from. One entry, one primary source; add a second only when it corrected the first.

## Confidence

- A field that rests on one summary read, or on memory of the work, carries `(unverified)`.
- Leave out anything about unreleased material: announced seasons, leaks, rumours.
- When two sources disagree, the work itself wins over official material, official material over the wiki, and the disagreement goes in the entry's `what` only if it matters to the target.

## Tier

Fame with the work's audience. Good evidence: views of clips titled with the thing's name, wiki pages linking to it, memes, merchandise, a poll of real viewers. A thing the whole plot of one unit turns on is not iconic for that reason: that is `story_weight`, which the index derives from moments.

## Rights

The bible holds facts and short quotes for internal use. Reference images, scripts and scans stay in `refs/` and out of any public repo: `.gitignore` covers `refs/`.
