---
name: chatdoc
description: Create, present through wslview, or migrate chat documents in a maintained project archive. Render HTML only by default; produce Markdown when explicitly requested.
---

# Chat documents

Keep chat reports, explanations, reviews and chat-only plans in the current project's `.agents/chatdocs/`. Read applicable repository instructions and inspect the existing archive before choosing names, renderers or index structure.

## Choose the format

An explicit format or filename requirement takes precedence over the default.

| Request | Output |
| --- | --- |
| No format specified, or `wslview` alone | HTML only |
| Markdown requested without a browser presentation | Markdown |
| Both Markdown and HTML requested | Both, with matching basenames |
| Markdown requested and presentation through `wslview` requested | Markdown plus HTML for the viewer |

The HTML default includes new indexes: create `index.html`, adding `index.md` only when explicitly requested. Preserve existing Markdown reports and indexes. Maintain existing indexes and link only formats actually present. Existing pairs do not require new reports to have a Markdown companion.

## Place and preserve

Keep related diagrams, scripts and data alongside the document. Preserve dates, source references, evidence identities, qualifications and unresolved limits. Keep distinct versions under distinct names; compare existing content before replacing a file. When producing both formats, use matching basenames such as `fault-review.md` and `fault-review.html`.

Canonical designs, implementation plans and qualification evidence belong where the repository specifies. Existing documents under `./docs/` stay in place even when opened through `wslview`. Identify the canonical source of an archival presentation copy. An archive request authorizes work on the requested chat documents and assets only.

## Create and present

Produce the selected formats using available project tools or a self-contained implementation. Write HTML directly by default. If a renderer uses Markdown internally, keep that input transient instead of saving an unrequested Markdown source, draft or sidecar. Preserve necessary diagrams, styling, scripts, data and interactive controls. Prefer existing tools and local assets; rendering does not require unrelated dependency installation or permanent workspace configuration.

Use relative links between archive documents and assets, adjusting paths after relocation. Validate each retained or produced format: local documents and resources exist, fragments resolve, and index links reach the intended versions. Include HTML references to scripts, stylesheets, images and data. Exercise relevant interactive controls when a browser is available; report untested behavior accurately.

For a browser presentation, run `wslview` on the completed HTML path after validation. Confirm launch success before saying the document opened, and distinguish launch from visual inspection. A Markdown-only request can be delivered with a file link. If presentation fails, retain the completed artifacts and report the failed action with usable links.

## Migrate an archive

Inventory the entire requested scope using files, existing indexes, links and available conversation records, including older reports. Account for each candidate's source, destination, assets and disposition.

Migrate existing formats as found, retaining Markdown originals and interactive assets. Generate a missing companion format only when requested or needed for a requested browser presentation. For cleared files, recover retained text and data when available. Read historical commands as evidence; never execute them to reconstruct a document. Label reconstructed portions, preserve historical dates and disclose gaps. Restoration does not establish fresh analysis or validation.

Move or copy according to canonical status, repair incoming links and update affected renderings and indexes. Verify all retained and generated destinations before removing source chat copies for a requested move. Canonical originals stay in place.

## Finish

When asked to establish the convention in `AGENTS.md`, inspect the existing file and adjust only the relevant instructions. Use the environment's escalation mechanism for protected destinations. Commit and push only when requested.

Report the archive location, index, presentation result and any missing sources or validation limits.
