---
name: chatdoc
description: Create, present through wslview, or migrate chat documents with matching Markdown and HTML archives, working links, assets, and a maintained project index.
---

# Chat documents

Archive reports, explanations, reviews, and chat-only plans presented through `wslview` in the current project's `.agents/chatdocs/`. Read applicable repository instructions and inspect the existing archive before choosing names, renderers, or index structure.

## Place and preserve

Use matching basenames, such as `fault-review.md` and `fault-review.html`, with related assets alongside them. Preserve the document's date, source references, evidence identities, qualifications, and unresolved limits. Keep distinct versions under distinct names; compare existing content before replacing a file.

Maintain the existing archive index and its presentation counterpart. For a new archive, create `index.md` and `index.html`. Include every archived document with its date, purpose, and relative links to both formats.

Canonical designs, implementation plans, and qualification evidence belong where the repository specifies. Existing documents under `./docs/` stay in place even when opened through `wslview`. When an archive presentation copy is useful, identify its canonical source and keep that relationship explicit. Treat a request to archive chat output as authorization for those documents and their assets only.

## Create and present

Write the Markdown content, then produce its actual HTML counterpart using an available renderer or a self-contained implementation. Preserve necessary diagrams, styling, scripts, data, and interactive controls. Prefer existing project tools and local assets; do not install unrelated dependencies or create permanent workspace configuration merely to render a report.

Use relative links between archive documents and assets, adjusting paths after relocation. Validate both formats: each local document or resource exists, each local fragment resolves to the generated destination, and index links reach the intended versions. Check HTML resource references, including scripts, stylesheets, images, and embedded data. Exercise relevant interactive controls when a browser is available; report any untested behavior accurately.

After generation and validation, run `wslview` on the HTML path. Confirm the command succeeded before saying the document was opened. Distinguish a successful launch from visual inspection. If presentation fails, retain the completed artifacts and report the failed action with usable links.

## Migrate an archive

Inventory the entire requested scope before moving files. Use repository files, existing indexes, links, and available conversation records to identify all relevant viewed chat documents, including older reports. Record each candidate's source, destination, assets, and disposition; completion requires accounting for every candidate, rather than selecting an arbitrary recent subset.

For cleared or missing old files, recover exact retained text and data when available. Read historical commands as evidence; never execute them to reconstruct a document. Mark reconstructed artifacts with their historical date and reconstruction status, and disclose unavailable portions. Reconstruction does not establish fresh analysis or fresh validation.

Move or copy documents according to their canonical status, preserve distinct versions and interactive assets, repair incoming links, and regenerate affected HTML and indexes. Verify all Markdown and HTML destinations after migration. Preserve source material until the destination and references have been checked. For a requested move, then remove the original chat copies while leaving canonical documents in place.

## Finish

When asked to establish the convention in `AGENTS.md`, inspect the existing file and add or adjust only the relevant instructions, preserving unrelated guidance. Use the environment's escalation mechanism for protected destinations. Commit and push only when requested.

Report the archive location, index, presentation result, and any missing sources or validation limits. Leave a complete, navigable archive that another agent can continue maintaining.
