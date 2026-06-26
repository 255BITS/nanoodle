# Inpaint model verification — which NanoGPT models honor a brushed mask

**Verified live: 2026-06-26** (re-run when NanoGPT's catalog changes).

## Why this exists

The Inpaint node sends `maskDataUrl` (white = repaint) to `POST /v1/images/generations`.
A model "honors" the mask when it repaints **only** the masked region and leaves the rest of the
image untouched. The catalog has **no metadata flag** for this, and model *descriptions* lie —
ideogram-v2/v3/v4 advertise "state of the art inpainting" yet repaint the **entire** image (or 500)
when handed a mask. So `index.html`'s `INPAINT_OK` allowlist is derived empirically, not from metadata.

## Method

`proof/harness/verify-inpaint-mask.py` (needs `NANOGPT_API_KEY` + Pillow; `python3 proof/harness/verify-inpaint-mask.py`):

1. Build a 512×512 **source**: blue field + a yellow circle top-left (a landmark *outside* the mask).
2. Build a **mask**: black, with a white square over the centre (~30% of the frame).
3. For each candidate, POST `{model, prompt:"a single bright red apple, centered", imageDataUrl, maskDataUrl}`.
4. Decode the result, measure mean per-pixel change **inside** the mask (want high — it edited) vs
   **outside** the mask (want ~0 — it left the rest alone).

**Decision rule:** ship a model only if `Δoutside < 6` and `Δinside > 12` (clean honorer). Models that
change the whole frame (`Δoutside ≳ 20`) or error are excluded. 73 edit/i2i candidates tested.

> `flux-lora/inpainting` (the only id literally matching `/inpaint/`) stays included via `needsMask`
> even though it scored Δinside≈4 (it preserves the mask but barely edits — "results are often not
> great", per its own description). It's the canonical fallback; the allowlist models are far better.

### Tier A — clean honorers (out<6, in>12) → shipped in INPAINT_OK
| model | Δ inside (want high) | Δ outside (want ~0) | ratio |
|---|---|---|---|
| `bria-fibo` | 77.7 | 0.0 | 776.5 |
| `bria-fibo-edit` | 77.7 | 0.0 | 777.1 |
| `nano-banana` | 48.1 | 1.2 | 40.0 |
| `reve-2-edit` | 75.9 | 1.2 | 62.7 |
| `nano-banana-pro` | 31.1 | 1.3 | 23.9 |
| `pruna-ai/p-image/edit-lora` | 90.2 | 1.6 | 55.3 |
| `pruna-ai/p-image/edit` | 85.6 | 1.7 | 51.8 |
| `nano-banana-2` | 81.8 | 1.7 | 49.3 |
| `kling-image-o1` | 107.6 | 1.7 | 61.6 |
| `nano-banana-edit` | 73.5 | 2.1 | 35.6 |
| `fal-ai/boogu-image/edit` | 61.0 | 2.3 | 26.5 |
| `reve-2-remix` | 89.0 | 2.3 | 38.0 |
| `gemini-flash-edit` | 70.4 | 2.3 | 31.1 |
| `nano-banana-pro-edit` | 86.0 | 2.7 | 32.3 |
| `imagineart/imagineart-2.0-edit-preview/image-to-image` | 66.0 | 3.4 | 19.5 |
| `nano-banana-pro-edit-ultra` | 28.4 | 3.6 | 8.0 |
| `flux-kontext` | 85.2 | 4.6 | 18.6 |

### Tier B — honor the mask but bleed (out 6–20) → NOT shipped (quality bar)
| model | Δ inside | Δ outside | ratio |
|---|---|---|---|
| `grok-imagine-image` | 70.9 | 8.4 | 8.5 |
| `hunyuan-image-3-instruct` | 103.7 | 8.5 | 12.1 |
| `xai/grok-imagine-image/quality/edit` | 78.6 | 8.7 | 9.1 |
| `qwen-image-2.0-pro` | 43.6 | 8.8 | 4.9 |
| `reve-2-edit-fast` | 90.7 | 9.3 | 9.8 |
| `riverflow-2.0-pro` | 81.7 | 9.5 | 8.6 |
| `seedream-v5.0-lite` | 98.2 | 10.6 | 9.3 |
| `nano-banana-2-fast` | 87.4 | 11.2 | 7.8 |
| `luma/agent/uni-1/v1` | 87.8 | 11.3 | 7.7 |
| `microsoft/mai-image-2.5/edit` | 89.9 | 11.7 | 7.7 |
| `seedream-v4.5-sequential` | 72.4 | 12.4 | 5.8 |
| `wavespeed-ai/flux-2-klein-base-4b/edit` | 110.1 | 14.2 | 7.7 |
| `seedream-4.5-alternative` | 98.1 | 14.7 | 6.7 |
| `step-image-edit-2` | 90.0 | 15.3 | 5.9 |
| `wavespeed-ai/flux-2-klein-base-9b/edit-lora` | 106.5 | 15.3 | 7.0 |
| `flux-2-max-image-to-image` | 65.8 | 16.1 | 4.1 |
| `gpt-4o-image` | 113.3 | 18.5 | 6.1 |

### Ignore the mask — repaint the whole image (out≥~20) → excluded
| model | Δ inside | Δ outside |
|---|---|---|
| `flux-lora/inpainting` | 3.7 | 1.3 |
| `z-image-turbo-image-to-image` | 2.8 | 2.0 |
| `flux-2-flex-image-to-image` | 106.4 | 21.1 |
| `flux-2-pro-image-to-image` | 85.6 | 22.2 |
| `flux-2-dev-lora-image-to-image` | 104.8 | 23.0 |
| `wavespeed-ai/flux-2-klein-base-4b/edit-lora` | 111.2 | 23.5 |
| `qwen-image` | 117.2 | 24.1 |
| `qwen-image-2.0` | 120.3 | 25.1 |
| `flux-2-dev-image-to-image` | 97.1 | 26.8 |
| `hidream-e1-1` | 19.0 | 27.0 |
| `flux-dev-image-to-image` | 60.4 | 29.0 |
| `flux-2-flash-image-to-image` | 100.5 | 34.1 |
| `flux-2-klein-9b` | 110.9 | 37.3 |
| `flux-2-turbo-image-to-image` | 98.8 | 43.4 |
| `wan-2.6-image-edit` | 112.5 | 44.0 |
| `wavespeed-ai/flux-2-klein-base-9b/edit` | 118.0 | 47.3 |
| `glm-image-edit` | 100.2 | 54.2 |
| `seedream-v4` | 112.5 | 59.0 |
| `minimax-image-01` | 105.2 | 71.2 |
| `hidream-o1-image-dev` | 91.5 | 76.5 |
| `hidream-o1-image` | 85.3 | 79.1 |
| `seedream-v4.5` | 84.6 | 107.7 |
| `reve-2-remix-fast` | 99.8 | 111.4 |
| `luma/agent/uni-1/v1/max` | 114.9 | 171.2 |
| `bagel` | 122.4 | 174.8 |

### Errored on the mask path → excluded
| model | error |
|---|---|
| `fal-ai/bernini-r/edit-image` | TimeoutError: The read operation timed out |
| `gpt-image-1.5` | 400: {"error":{"message":"Image generation failed. Please try a different prompt or image. |
| `seedream-v5.0-lite-sequential` | 400: {"error":"Seedream 5.0 Lite Sequential requires a minimum resolution of 2560x1440 pix |
| `wan2.7-image` | 400: {"error":"Image generation failed. Please try a different prompt or image.","type":"I |
| `wan2.7-image-pro` | 400: {"error":"Image generation failed. Please try a different prompt or image.","type":"I |
| `qwen-image-max-edit` | 400: {"error":"Image generation failed. Please try a different prompt or image.","type":"I |
| `riverflow-2-fast` | 400: {"error":{"message":"Image generation failed. Please try a different prompt or image. |
| `riverflow-2-standard` | 400: {"error":{"message":"Image generation failed. Please try a different prompt or image. |
| `gpt-image-1` | 400: {"error":{"message":"Image generation failed. Please try a different prompt or image. |
| `gpt-image-1-mini` | 400: {"error":"Image generation failed. Please try a different prompt or image.","type":"I |
| `gpt-image-2` | 400: {"error":"GPT Image 2 supports total pixels between 655,360 and 3,686,400.","type":"I |
| `reve-image-to-image` | 400: {"error":"Image generation failed. Please try a different prompt or image.","type":"I |
| `longcat-image-edit` | 504: {"error":"Request timed out. Please try again.","code":"request_timeout","type":"requ |
| `runwayml-gen4-image` | 400: {"error":"Image generation failed. Please try a different prompt or image.","type":"I |