# Directory & awesome-list submission drafts (paste-ready)

Rev 1 — 2026-07-11. Executes the "directory blitz" of `plan-q3-distribution.md`
Phase 1. One sitting each; log every submission in `shares.md`.

Rules baked into every block below: no "free" in CTA-style copy, disclosed
maker, BYOK/paid-API stated honestly, no third-party embeds pointed at
nanoodle.com. Facts checked against source 2026-07-11: MIT license, repo
public with full history, npm + PyPI package name is `nanoodle` on both.

**Canonical short description (reuse when a form wants "one paragraph"):**

> nanoodle is an open-source (MIT) node-graph editor for AI workflows that
> runs entirely in the browser — no server, no account, zero analytics. Wire
> text, image, video and audio models into a graph, run it client-side
> through your own nano-gpt.com API key (pay-per-call), then export the
> graph as a standalone single-file HTML app or share it as a URL where the
> graph lives in the fragment and never reaches a server.

**Canonical one-liner:** Browser-only node-graph editor for AI workflows —
single-file HTML export, zero analytics, bring-your-own API key. MIT.

---

## AlternativeTo

**URL:** https://alternativeto.net → "Add an application" (account created
Jul 11 per plan; ~1-week new-account cooldown → submit ~Jul 18).

- **Name:** nanoodle
- **Website:** https://nanoodle.com
- **Platforms:** Web, Self-Hosted (it's a static page; anyone can serve the
  repo themselves)
- **License:** Open Source (MIT) — source: https://github.com/nanoodlecom/nanoodle
- **Description:** canonical short description above.
- **Alternative to:** ComfyUI, n8n, Node-RED
- **Per-pair "how it differs" notes:**
  - *vs ComfyUI:* No install and no local GPU — the editor is a single
    static web page and models run via API. Trade-off: ComfyUI has a huge
    custom-node ecosystem and runs models locally; nanoodle wins on
    zero-setup, privacy (no telemetry, keys stay in your browser) and
    exporting a workflow as one self-contained .html app.
  - *vs n8n:* n8n is a general automation server with hundreds of
    integrations; nanoodle is a client-side canvas focused on multi-model
    AI pipelines (text/image/video/audio) with no server component at all.
  - *vs Node-RED:* Node-RED is a server-side flow runtime for
    IoT/integration; nanoodle is browser-only and AI-model-focused, and its
    output is a shareable URL or standalone HTML file rather than a running
    server.

## OpenAlternative.co

**URL:** https://openalternative.co/submit

- **Name:** nanoodle
- **Repository:** https://github.com/nanoodlecom/nanoodle
- **Website:** https://nanoodle.com
- **Alternative to:** ComfyUI
- **Description:** canonical short description.

## opensourcealternative.to

**URL:** https://www.opensourcealternative.to → "Submit a project"

- **Name:** nanoodle · **License:** MIT ·
  **Repo:** https://github.com/nanoodlecom/nanoodle ·
  **Site:** https://nanoodle.com
- **Alternative to:** ComfyUI (also fits: n8n, Node-RED for the AI-pipeline
  use case)
- **Description:** canonical short description.

## LibHunt (all three public repos, BEFORE the Jul 15 HN post)

**URL:** https://www.libhunt.com — use the suggest/add-project link on the
site; LibHunt then auto-tracks mentions.

1. **nanoodlecom/nanoodle** — Browser-only node-graph editor for AI
   workflows; the whole product is one static HTML page. MIT.
2. **nanoodlecom/nanoodle-js** — Zero-dependency JavaScript executor for
   nanoodle graphs (`npm install nanoodle`). Run a saved graph from Node
   without the editor.
3. **nanoodlecom/nanoodle-py** — Zero-dependency Python executor for
   nanoodle graphs (`pip install nanoodle`). Same graph JSON, same
   payloads, byte-parity-tested against the JS executor.

## SourceForge / Slashdot software directory

**URL:** https://sourceforge.net/software/ → vendor/product listing (the
same profile syndicates to the Slashdot software directory).

- **Product:** nanoodle · **Category:** AI / workflow automation
- **Description:** canonical short description, plus: "Runs as a static
  page; self-hosting is copying one directory to any web server."
- **Pricing field, answered honestly:** the software is open source (MIT);
  running AI models requires the user's own nano-gpt.com API key, billed
  per call by that provider. nanoodle itself has no plans or billing.

---

## Awesome-list one-line PR entries

Match the surrounding entry format exactly at PR time (bullet char, dash
style, trailing period); the content blocks below are the payload. One PR
per list, honest PR description ("maker of the project, disclosing that").

### xyflow/awesome-node-based-uis

**URL:** https://github.com/xyflow/awesome-node-based-uis

> [nanoodle](https://nanoodle.com) – Node-graph editor for AI pipelines
> (text/image/video/audio) that runs entirely in the browser and exports
> graphs as standalone single-file HTML apps. Open source (MIT).

### steven2358/awesome-generative-ai

**URL:** https://github.com/steven2358/awesome-generative-ai

> [nanoodle](https://nanoodle.com) - Browser-only node canvas for chaining
> generative text, image, video and audio models into workflows, with
> single-file HTML export. Bring your own API key.

### localfirstweb.dev

**URL:** https://github.com/localfirstweb/localfirstweb.dev — PR against
`_data/content.json`; entry shape verified 2026-07-11 (`title` / `author` /
`url` / `icon` inside a section's `items` array — pick the section that
matches at PR time):

```json
{
  "title": "nanoodle — node-graph AI workflows, fully client-side",
  "author": "nanoodle",
  "url": "https://nanoodle.com",
  "icon": "https://nanoodle.com/favicon-32.png"
}
```

Honest-fit note for the PR body: local-first in the sense of client-side
compute, IndexedDB persistence, zero analytics and single-file export;
model inference itself is a remote API (bring-your-own key) — stated so the
maintainers can judge fit.

### alexanderop/awesome-local-first

**URL:** https://github.com/alexanderop/awesome-local-first

> [nanoodle](https://nanoodle.com) - Node-graph AI workflow editor that
> runs entirely in the browser: IndexedDB persistence, share-links in URL
> fragments, standalone single-file HTML export, zero analytics. Model
> calls use your own API key. (MIT)

### pluja/awesome-privacy

**URL:** https://github.com/pluja/awesome-privacy (entry format verified
2026-07-11: `* [Name](url) - description.`)

> * [nanoodle](https://nanoodle.com) - Open source (MIT) node-graph editor
>   for AI workflows that runs fully in the browser: no account, no server,
>   zero analytics, CSP pinned to a single API origin. Your API key and
>   graphs stay in your browser; share-links live in the URL fragment and
>   never reach a server.

### awesome-privacy.xyz (Lissy93/awesome-privacy)

**URL:** https://github.com/Lissy93/awesome-privacy — data-driven repo;
follow its contribution flow (YAML data file / issue form, whichever the
CONTRIBUTING.md specifies at PR time). Payload values:

- name: nanoodle · url: https://nanoodle.com ·
  github: nanoodlecom/nanoodle · license: MIT
- description: as in the pluja entry above.
- disclosure line for the PR/issue: AI model calls go to nano-gpt.com with
  the user's own key (pay-per-call); everything else is client-side, and
  the CSP in the repo's `_headers` file is the auditable proof.

### ripienaar/free-for-dev

**URL:** https://github.com/ripienaar/free-for-dev — marginal fit (the plan
says accept a decline). Closest section: "Tools for Teams and
Collaboration" or "Design and UI" don't fit; propose under the APIs/dev
tools area only if maintainers agree the no-cost tier framing applies (the
editor, sharing and export have no cost; model execution is the user's own
API spend — say exactly that in the PR).

> [nanoodle.com](https://nanoodle.com) — Browser-based node-graph editor
> for AI workflows. The editor, URL sharing and single-file HTML export
> have no cost and need no account; running models uses your own
> nano-gpt.com API key (pay-per-call).

---

## Wikidata item

**URL:** https://www.wikidata.org/wiki/Special:NewItem (a data item is fine
where a Wikipedia article would fail notability — per plan skip-list).

- **Label (en):** nanoodle
- **Description (en):** browser-based open-source node-graph editor for AI
  workflows
- **Statements:**
  - instance of (P31): free software; web application
  - official website (P856): https://nanoodle.com
  - source code repository URL (P1324): https://github.com/nanoodlecom/nanoodle
  - copyright license (P275): MIT license
  - programming language (P277): JavaScript
  - inception (P571): 2026
- Add sitelinks/identifiers only when they exist (no padding). Reference
  each statement with the official website or the repository URL.
