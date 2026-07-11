# Newsletter / podcast / community pitch templates

Rev 1 — 2026-07-11. Used by `launch-runbook.md` day-after step. All five are
short, factual, disclosed-maker, zero hype-words, no "free" in CTA copy.
Personalize the greeting, keep the body under ~120 words — editors skim.

Fill-ins marked `{{like this}}`. Send from mikkel@255bits.com.

---

## 1. Console.dev (tool recommendation form)

**Where:** the "recommend a tool" form on https://console.dev

> **Tool:** nanoodle — https://nanoodle.com
> **What it is:** A node-graph editor for AI workflows (text/image/video/
> audio models) that runs entirely in the browser. No server, no account,
> zero analytics; the whole product is one static HTML page. Graphs export
> as standalone single-file .html apps and share as URLs where the graph
> lives in the fragment. Open source, MIT:
> https://github.com/nanoodlecom/nanoodle
> **Why interesting:** The single-file constraint forced unusual
> engineering — dual run-engines (editor + exported app) kept in parity by
> pre-commit hooks, auth via OAuth PKCE straight from the browser, and a
> CSP with no third-party origins as the enforceable privacy claim.
> **Disclosure:** I'm the maker. Bring-your-own nano-gpt.com API key,
> pay-per-call — that's the honest trade-off for having no backend.

## 2. JavaScript Weekly / Node Weekly (Cooperpress)

**Where:** the "suggest a link" / recommendation link in each issue's
footer. Angle: **mp4cat + the CLI** — a concrete zero-dep library story,
not a product ad. Send after the ~Aug 5 mp4cat launch.

> Subject: mp4cat — lossless MP4 concatenation in pure JS, zero deps
>
> Hi — maker here, suggesting my own project (disclosed). mp4cat joins MP4
> files losslessly by remuxing at the box level: no re-encode, no ffmpeg,
> no native bindings, zero dependencies. It exists because I needed video
> concatenation *inside the browser* for nanoodle (a client-side node-graph
> editor), so the same code runs in Node and in a page.
> Repo: https://github.com/nanoodlecom/mp4cat
> Related, if the CLI angle fits better: `npx nanoodle run <graph.json>`
> executes a visual AI pipeline from the terminal — the npm package
> (`nanoodle`) is also dependency-free. https://github.com/nanoodlecom/nanoodle-js
> Show HN discussion from launch: {{HN link}}

## 3. Changelog News (email pitch)

**Where:** the submit address linked from https://changelog.com/news.
Angle: **the single-file architecture story.**

> Subject: One HTML file as the whole product — nanoodle
>
> Hi {{editor name}} — story suggestion, and I'm the maker (disclosed).
> nanoodle is a node-graph AI workflow editor where the entire product is a
> single static HTML page: no build step, no backend, zero analytics. The
> constraint produced the interesting engineering — exported apps embed
> their own runtime inside a String.raw template (one stray backtick breaks
> every export, so a pre-commit hook exists solely to hunt backticks),
> editor and export are twin run-engines held in parity by hooks, and the
> privacy claim is enforced by a CSP with no third-party origins rather
> than by a policy page.
> MIT, full history public: https://github.com/nanoodlecom/nanoodle
> Live: https://nanoodle.com — happy to provide more detail or a q&a.

## 4. devtools.fm (podcast guest pitch)

**Where:** guest suggestion route on https://devtools.fm (form or the
contact listed there).

> Subject: Guest pitch: browser-only node-graph editor, one HTML file, no
> server, no analytics — one person + AI agents
>
> Hi Andrew & Justin — I'm Mikkel, maker of nanoodle
> (https://nanoodle.com, MIT: https://github.com/nanoodlecom/nanoodle).
> It's a ComfyUI-style node canvas for AI pipelines that ships as one
> static HTML page: OAuth PKCE from the browser, IndexedDB persistence,
> share-links in URL fragments, graphs exportable as standalone .html apps.
> Two threads I can go deep on:
> 1. What a genuinely serverless (as in: *no* server) product forces you to
>    design differently — auth, persistence, sharing, privacy-as-CSP.
> 2. The workflow: it's built by one person orchestrating AI agents, with
>    40 pre-commit guards doing the code review a team would — the growth
>    planning happens in the open in the repo too.
> Disclosure for listeners: bring-your-own API key (nano-gpt.com,
> pay-per-call); no subscription, no analytics.

## 5. daily.dev Squad post

**Where:** the relevant Squad on https://daily.dev (post as maker, say so).

> **Title:** I built a node-graph AI editor that is literally one HTML file
>
> Maker post, honest version: nanoodle is a ComfyUI-style canvas for
> text/image/video/audio pipelines that runs 100% in the browser. No
> server, no account, zero analytics — the CSP has no third-party origins,
> so the network tab is the proof. Graphs export as standalone single-file
> .html apps and share as URLs (the graph is in the fragment; it never
> reaches a server). Trade-off, stated upfront: models run through your own
> nano-gpt.com API key, pay-per-call.
> Source (MIT): https://github.com/nanoodlecom/nanoodle
> Try it: https://nanoodle.com — feedback on the single-file architecture
> especially welcome.
