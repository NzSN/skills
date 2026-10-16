## What it does

`chatdoc` saves chat reports, explanations, reviews and chat-only plans as HTML by default in your project's `.agents/chatdocs/` directory. Existing files under `docs/` stay at their original paths, even when you open them through `wslview`.

Markdown is produced when explicitly requested. The archive keeps an index, related assets and the dates and limits of older reports. Temporary files can be cleared without losing the delivered explanation.

## When to reach for it

Type `/chatdoc`, or it is selected automatically when a document-presentation request fits.

- Ask for an explanation opened through `wslview`, with HTML as the default output.
- Gather earlier chat documents into a durable project archive.
- Recover a previous explanation whose temporary copy has disappeared.

## Prerequisites

A project directory to hold `.agents/chatdocs/`. Opening the browser presentation requires WSL with `wslview`; the saved files remain usable if launching the viewer fails.

## The archive

A new report is an HTML file, with diagrams, scripts and data kept alongside it. When both Markdown and HTML are requested, their files share a basename. An existing index keeps its name and structure; new archives start with `index.html`. A Markdown index is added only when requested.

Archiving earlier reports starts with an inventory of the requested scope. Distinct versions keep distinct names. Existing Markdown reports and indexes are preserved during migration. Canonical designs, plans and evidence retain their repository owners; presentation copies identify their source.

## Common questions

**Does every report need Markdown as well as HTML?**

No. With no explicit format requirement, the output is HTML only, including a new archive index. Ask for Markdown, both formats or a specific filename when needed. A Markdown request with a `wslview` presentation produces both, since the viewer opens HTML.

**Will it move files already under `docs/`?**

Those files stay in place. The archive contains chat documents and, where useful, a clearly identified presentation copy of a canonical document.

**What if the old files in `/tmp` were cleared?**

It looks for retained files, original conversation text and recorded data. Reconstructed portions are labeled, missing portions are reported, and historical results keep their original date. Restoring a page does not rerun its analysis.

**Is the folder `agents` or `.agents`?**

Use `.agents/chatdocs/` inside the project. Related assets and the archive index live there too.

## It's working if

- A default presentation produces HTML without an extra Markdown companion.
- The index reopens every delivered report from the project archive.
- Links and interactive controls still work after a move.
- Existing `docs/` documents remain at their original paths.
- Older reports retain their dates and state which parts were reconstructed.

## Where it fits

This is a reach-for-it-anytime standalone workflow for presenting and retaining conversation output. Use [writing-for-agents](https://aihero.dev/skills-writing-for-agents) for the wording of instructions such as an `AGENTS.md` convention. [ask-matt](https://aihero.dev/skills-ask-matt) helps choose among the wider skill set.
