## What it does

`chatdoc` saves chat reports, explanations, reviews and chat-only plans as Markdown and HTML in your project's `.agents/chatdocs/` directory. Existing files under `docs/` stay at their original paths, even when you open them through `wslview`.

The archive keeps an index, related assets and the dates and limits of older reports. Temporary files can be cleared without losing the delivered explanation.

## When to reach for it

Type `/chatdoc`, or it is selected automatically when a document-presentation request fits.

- Ask for an answer as Markdown and HTML, opened through `wslview`.
- Gather earlier chat documents into a durable project archive.
- Recover a previous explanation whose temporary copy has disappeared.

## Prerequisites

A project directory to hold `.agents/chatdocs/`. Opening the browser presentation requires WSL with `wslview`; the saved files remain usable if launching the viewer fails.

## The archive

The Markdown and browser page share a basename, with diagrams, scripts and data kept alongside them. An existing index keeps its name and structure. New archives start with `index.md` and `index.html`.

Archiving earlier reports starts with an inventory of the requested scope. Distinct versions keep distinct names. Canonical designs, plans and evidence retain their repository owners; presentation copies identify their source.

## Common questions

**Will it move files already under `docs/`?**

Those files stay in place. The archive contains chat documents and, where useful, a clearly identified presentation copy of a canonical document.

**What if the old files in `/tmp` were cleared?**

It looks for retained files, original conversation text and recorded data. Reconstructed portions are labeled, missing portions are reported, and historical results keep their original date. Restoring a page does not rerun its analysis.

**Is the folder `agents` or `.agents`?**

Use `.agents/chatdocs/` inside the project. Related assets and the Markdown/HTML index live there too.

## It's working if

- The index reopens every delivered report from the project archive.
- Links and interactive controls still work after a move.
- Existing `docs/` documents remain at their original paths.
- Older reports retain their dates and state which parts were reconstructed.

## Where it fits

This is a reach-for-it-anytime standalone workflow for presenting and retaining conversation output. Use [writing-for-agents](https://aihero.dev/skills-writing-for-agents) for the wording of instructions such as an `AGENTS.md` convention. [ask-matt](https://aihero.dev/skills-ask-matt) helps choose among the wider skill set.
