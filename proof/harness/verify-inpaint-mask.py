#!/usr/bin/env python3
"""
verify-inpaint-mask.py  —  Mask-honoring test for NanoGPT image-edit models.

For every image edit candidate in the live catalog, sends:
  imageDataUrl  = a simple gray-grid source image (1024x1024)
  maskDataUrl   = a white ellipse in the centre (~33% margin, edit zone)
  prompt        = "fill the white ellipse region with vibrant solid red paint"

Measures mean absolute pixel change INSIDE vs OUTSIDE the ellipse at 256x256
(grayscale downsampled, via ImageChops.difference).

  in_score  = mean change inside the white mask region
  out_score = mean change outside the white mask region

Models that honour the mask paint only inside → in >> 0, out ≈ 0.
Models that regenerate the whole image    → both scores are large & similar.

Writes:  proof/harness/batch_results.json
Also saves (for debugging, do NOT commit):
  b_source.png     — source image fed to every model
  b_mask.png       — mask image fed to every model
  ip_<slug>.png    — result image from each passing model
  cands.json       — list of model ids tested

Usage:
  export NANOGPT_API_KEY=sk-...
  python3 proof/harness/verify-inpaint-mask.py
"""

import json, os, sys, io, base64, re, time

import requests
from PIL import Image, ImageDraw, ImageChops

# numpy is optional — greatly speeds up pixel diff
try:
    import numpy as np
    _NP = True
except ImportError:
    _NP = False

# ── config ───────────────────────────────────────────────────────────────────
API_KEY = os.environ.get("NANOGPT_API_KEY", "")
if not API_KEY:
    print("ERROR: NANOGPT_API_KEY not set", file=sys.stderr)
    sys.exit(1)

NANOGPT      = "https://nano-gpt.com"
IMG_ENDPOINT = f"{NANOGPT}/v1/images/generations"
IMG_CATALOG  = f"{NANOGPT}/api/v1/image-models"

SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
OUT_JSON     = os.path.join(SCRIPT_DIR, "batch_results.json")
CANDS_JSON   = os.path.join(SCRIPT_DIR, "cands.json")

IMG_SIZE     = 1024   # generation size sent to the API
CMP_SIZE     = 256    # downsample for fast pixel comparison

PROMPT       = "fill the white ellipse region with vibrant solid red paint"

# ── image builders ───────────────────────────────────────────────────────────
def make_source(size=IMG_SIZE):
    """Gray-grid canvas — structured enough to detect global vs local change."""
    img  = Image.new("RGB", (size, size), (200, 200, 200))
    draw = ImageDraw.Draw(img)
    for i in range(0, size, 128):
        draw.line([(i, 0), (i, size)], fill=(155, 155, 155), width=2)
        draw.line([(0, i), (size, i)], fill=(155, 155, 155), width=2)
    return img

def make_mask(size=IMG_SIZE):
    """Black canvas with a white ellipse in the centre (edit zone).
    Margin ≈ 33% on each side → ellipse covers the middle ~33% of the image.
    White = region to repaint (matches NanoGPT / fal maskDataUrl convention).
    """
    mask = Image.new("RGB", (size, size), (0, 0, 0))
    m    = size // 3
    ImageDraw.Draw(mask).ellipse([m, m, size - m, size - m], fill=(255, 255, 255))
    return mask

def to_data_url(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

def b64_to_img(b64: str) -> Image.Image:
    return Image.open(io.BytesIO(base64.b64decode(b64)))

# ── pixel diff ───────────────────────────────────────────────────────────────
def measure_diff(orig: Image.Image, result: Image.Image, mask: Image.Image):
    """Return (in_score, out_score).
    Scores are mean absolute grayscale pixel change at CMP_SIZE resolution.
    """
    sz  = (CMP_SIZE, CMP_SIZE)
    og  = orig.convert("L").resize(sz, Image.LANCZOS)
    rs  = result.convert("L").resize(sz, Image.LANCZOS)
    mk  = mask.convert("L").resize(sz, Image.NEAREST)
    dif = ImageChops.difference(og, rs)

    if _NP:
        d   = np.array(dif, dtype=float)
        m   = np.array(mk)
        ins = m > 127
        out = ~ins
        return (float(d[ins].mean()) if ins.any() else 0.0,
                float(d[out].mean()) if out.any() else 0.0)

    # pure-Python fallback
    dp = dif.load()
    mp = mk.load()
    it = ic = ot = oc = 0
    for y in range(CMP_SIZE):
        for x in range(CMP_SIZE):
            d = dp[x, y]
            if mp[x, y] > 127:
                it += d; ic += 1
            else:
                ot += d; oc += 1
    return ((it / ic) if ic else 0.0, (ot / oc) if oc else 0.0)

# ── catalog ──────────────────────────────────────────────────────────────────
def fetch_catalog():
    r = requests.get(
        IMG_CATALOG,
        headers={"Authorization": f"Bearer {API_KEY}"},
        timeout=30,
    )
    r.raise_for_status()
    data = r.json().get("data")
    if not isinstance(data, list):
        raise ValueError(f"Unexpected catalog shape: {str(r.text)[:300]}")
    return data

def is_edit_candidate(m: dict) -> bool:
    """True if the model accepts an image input (edit / img2img / upscale)."""
    mid  = m.get("id", "")
    caps = m.get("capabilities") or {}
    return (
        bool(re.search(r"upscal|image-to-image|img2img", mid, re.I))
        or bool(caps.get("image_to_image"))
    )

# ── per-model call ────────────────────────────────────────────────────────────
def test_one(model_id: str, src_url: str, mask_url: str,
             src_img: Image.Image, mask_img: Image.Image):
    """Return (in_score, out_score, result_img) or raise."""
    body = {
        "model":           model_id,
        "prompt":          PROMPT,
        "size":            "1024x1024",
        "n":               1,
        "response_format": "b64_json",
        "imageDataUrl":    src_url,
        "maskDataUrl":     mask_url,
    }
    hdrs = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type":  "application/json",
    }
    r = requests.post(IMG_ENDPOINT, headers=hdrs, json=body, timeout=180)
    if not r.ok:
        raise RuntimeError(f"HTTP {r.status_code}: {r.text[:300]}")

    j     = r.json()
    items = j.get("data") or []
    if not items:
        raise RuntimeError(f"Empty data in response: {str(j)[:300]}")

    d   = items[0]
    b64 = d.get("b64_json")
    if b64:
        result_img = b64_to_img(b64)
    else:
        url = d.get("url")
        if not url:
            raise RuntimeError(f"No b64_json or url in response item: {str(d)[:300]}")
        rr = requests.get(url, timeout=60)
        rr.raise_for_status()
        result_img = Image.open(io.BytesIO(rr.content))

    in_s, out_s = measure_diff(src_img, result_img, mask_img)
    return in_s, out_s, result_img

# ── main ──────────────────────────────────────────────────────────────────────
def main():
    print("=== verify-inpaint-mask.py ===")

    # 1. Fetch catalog
    print(f"\n[1/3] Fetching catalog from {IMG_CATALOG} …")
    try:
        all_models = fetch_catalog()
    except Exception as exc:
        print(f"FATAL: catalog fetch failed: {exc}", file=sys.stderr)
        sys.exit(2)

    candidates = [m for m in all_models if is_edit_candidate(m)]
    print(f"  {len(all_models)} total models → {len(candidates)} edit candidates")

    with open(CANDS_JSON, "w") as f:
        json.dump([m["id"] for m in candidates], f, indent=2)

    # 2. Build test images
    print("\n[2/3] Building source + mask images …")
    src_img  = make_source()
    mask_img = make_mask()
    src_url  = to_data_url(src_img)
    mask_url = to_data_url(mask_img)
    src_img.save(os.path.join(SCRIPT_DIR, "b_source.png"))
    mask_img.save(os.path.join(SCRIPT_DIR, "b_mask.png"))

    # 3. Test each candidate
    print(f"\n[3/3] Testing {len(candidates)} models …")
    results = []
    for i, m in enumerate(candidates):
        mid   = m["id"]
        label = f"[{i+1}/{len(candidates)}]"
        print(f"{label} {mid} … ", end="", flush=True)
        t0 = time.time()
        try:
            in_s, out_s, res_img = test_one(mid, src_url, mask_url, src_img, mask_img)
            elapsed = time.time() - t0
            print(f"in={in_s:.2f}  out={out_s:.2f}  ({elapsed:.1f}s)")
            slug = re.sub(r"[^a-zA-Z0-9_.-]", "_", mid)[:48]
            res_img.save(os.path.join(SCRIPT_DIR, f"ip_{slug}.png"))
            results.append({
                "model": mid,
                "in":    round(in_s, 3),
                "out":   round(out_s, 3),
                "error": None,
            })
        except Exception as exc:
            elapsed = time.time() - t0
            print(f"ERROR ({elapsed:.1f}s): {exc}")
            results.append({
                "model": mid,
                "in":    None,
                "out":   None,
                "error": str(exc),
            })
        if i < len(candidates) - 1:
            time.sleep(0.5)

    # Write results
    with open(OUT_JSON, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults written → {OUT_JSON}")

    # Print summary
    passing = [r for r in results
               if r["in"] is not None and r["out"] is not None
               and r["in"] > 12 and r["out"] < 6
               and not re.search(r"inpaint", r["model"], re.I)]
    ignoring = [r for r in results
                if r["error"] is None
                and not re.search(r"inpaint", r["model"], re.I)
                and not (r["in"] is not None and r["out"] is not None
                         and r["in"] > 12 and r["out"] < 6)]
    errored  = [r for r in results if r["error"]]

    print(f"\n{'='*60}")
    print(f"Tier A — mask honoured (out<6 and in>12): {len(passing)}")
    for r in passing:
        print(f"  ✓  {r['model']:50s}  in={r['in']:.2f}  out={r['out']:.2f}")
    print(f"\nIgnores mask / global regen:  {len(ignoring)}")
    for r in ignoring:
        s = f"in={r['in']:.2f}  out={r['out']:.2f}" if r["in"] is not None else "no score"
        print(f"  ✗  {r['model']:50s}  {s}")
    print(f"\nErrored:  {len(errored)}")
    for r in errored:
        print(f"  !  {r['model']:50s}  {str(r['error'])[:80]}")

if __name__ == "__main__":
    main()
