# AlternativeTo listing

> DRAFT — for a human to submit at https://alternativeto.net/manage-item/
> (requires an AlternativeTo account). Drafted 2026-07-17. AlternativeTo is
> slow-burn SEO, not a launch spike — submit any time; no timing pressure.

## Listing fields

**Name:** nanoodle

**URL:** https://nanoodle.com

**Short description (one line):**

Node-graph AI workflow editor that runs entirely in the browser — no server,
no signup, no analytics; export any workflow as a standalone HTML app.

**Full description:**

nanoodle is a client-side-only node canvas for chaining AI models (LLM, image,
video, audio/TTS) into workflows. Everything runs in your browser: there is no
backend, no account system, and no analytics. You bring your own NanoGPT
(nano-gpt.com) API key — paste it or sign in via OAuth — and pay the provider
per call; nanoodle never sees your key, prompts, or outputs.

Workflows are shared as URLs (the graph is encoded in the URL fragment, which
never reaches a server) or exported as a single self-contained .html file you
can host anywhere or open from disk. The same graph format also runs headlessly
via the `nanoodle` package on npm (0.4.0) and PyPI (0.2.0), and there's an MCP
server and a GitHub Action.

Open source (MIT) — the site is served straight from its repository, and the
whole ecosystem (11+ repos) is public at https://github.com/nanoodlecom.

**License:** Open Source (MIT)

**Platforms:** Online (web); Self-Hosted (it's a static folder — any file
server works)

**Pricing:** Free (the app itself; running models uses your own NanoGPT key,
pay-per-call). On AlternativeTo pick "Free • Open Source" and note the BYO-key
cost in the description — do not present it as fully free to operate.

**Tags/categories:** ai-workflow, node-editor, no-code, privacy, browser-based,
text-to-image, workflow-automation

## "Alternative to" entries

Add nanoodle as an alternative to (only where the claim is defensible — we
have comparison pages for the first two):

- **ComfyUI** — same node-graph idiom, but cloud models via API instead of a
  local GPU; see https://nanoodle.com/nanoodle-vs-comfyui and
  https://nanoodle.com/comfyui-alternative
- **n8n** — for AI-chain use cases only; see https://nanoodle.com/nanoodle-vs-n8n

Don't claim it as an alternative to full automation platforms (Zapier etc.) —
nanoodle has no triggers/integrations and the listing will get disputed.

## Notes for the submitter

- AlternativeTo entries are community-moderated; a plain, accurate description
  survives review better than marketing copy.
- Add 2–3 screenshots: the editor canvas with a wired graph, an exported app
  running, the share dialog (reuse the Product Hunt gallery assets in
  `shareassets/`).
- Once live, log the URL in shares.md and link it from the launch runbook.
