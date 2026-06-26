import os, io, json, base64, re, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageChops

KEY = os.environ["NANOGPT_API_KEY"]
ENDPOINT = "https://nano-gpt.com/v1/images/generations"
OUT = os.path.dirname(os.path.abspath(__file__))
W = H = 512
mx0, my0, mx1, my1 = int(W*0.34), int(H*0.34), int(W*0.66), int(H*0.66)

src = Image.new("RGB", (W, H), (24, 64, 200))
d = ImageDraw.Draw(src)
d.ellipse([40, 40, 150, 150], fill=(245, 210, 30))
d.rectangle([mx0, my0, mx1, my1], outline=(255,255,255), width=2)
mask = Image.new("RGB", (W, H), (0,0,0))
ImageDraw.Draw(mask).rectangle([mx0, my0, mx1, my1], fill=(255,255,255))
inside = mask.convert("L").point(lambda p: 255 if p>127 else 0)

def data_url(img):
    b = io.BytesIO(); img.save(b, format="PNG")
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()
src_url, mask_url = data_url(src), data_url(mask)
PROMPT = "a single bright red apple, centered"

def region_diff(out):
    out = out.convert("RGB").resize((W,H))
    diff = ImageChops.difference(src.convert("RGB"), out).convert("L")
    pd, pm = diff.load(), inside.load(); sin=cin=sout=cout=0
    for y in range(0,H,3):
        for x in range(0,W,3):
            v=pd[x,y]
            if pm[x,y]>127: sin+=v; cin+=1
            else: sout+=v; cout+=1
    return (sin/max(cin,1), sout/max(cout,1))

def call(model):
    body=json.dumps({"model":model,"prompt":PROMPT,"size":f"{W}x{H}","n":1,
        "response_format":"b64_json","imageDataUrl":src_url,"maskDataUrl":mask_url}).encode()
    req=urllib.request.Request(ENDPOINT,data=body,method="POST",
        headers={"Authorization":f"Bearer {KEY}","x-api-key":KEY,"Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req,timeout=240) as r: j=json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return {"model":model,"ok":False,"err":f"{e.code}: "+e.read().decode()[:120]}
    except Exception as e:
        return {"model":model,"ok":False,"err":f"{type(e).__name__}: {e}"[:140]}
    d0=(j.get("data") or [{}])[0]; b64=d0.get("b64_json")
    if not b64 and d0.get("url"):
        try: b64=base64.b64encode(urllib.request.urlopen(d0["url"],timeout=60).read()).decode()
        except Exception as e: return {"model":model,"ok":False,"err":f"url:{e}"[:120]}
    if not b64: return {"model":model,"ok":False,"err":"no image in response"}
    try:
        img=Image.open(io.BytesIO(base64.b64decode(b64)))
        img.convert("RGB").save(os.path.join(OUT,"b_"+re.sub(r'[^A-Za-z0-9]','_',model)+".png"))
        din,dout=region_diff(img)
    except Exception as e:
        return {"model":model,"ok":False,"err":f"decode:{e}"[:120]}
    honors = dout < 20 and din > 12
    return {"model":model,"ok":True,"in":round(din,1),"out":round(dout,1),
            "ratio":round(din/max(dout,0.1),1),"honors":honors,
            "weak": din < 18}

# Discover candidates from the live catalog: anything that can take a source image (i2i capability,
# image->image modality, or edit/inpaint/mask/etc. in id|description), minus non-inpaint families
# (upscalers, bg-removers, vectorizers, crop, vto, text-to-image-only).
def candidates():
    raw = json.loads(urllib.request.urlopen("https://nano-gpt.com/api/v1/image-models", timeout=60).read())
    data = raw.get("data", raw)
    keep = re.compile(r'image->image|text\+image->image', re.I)
    hint = re.compile(r'\bedit|inpaint|mask|fill|retouch|replace', re.I)
    drop = re.compile(r'upscal|clarity|seedvr|background-remover|ghiblify|cropper|remove-text|text-to-vector|/vto|text-to-image|Upscaler|recraft', re.I)
    out=[]
    for m in data:
        mid=m.get("id",""); mod=(m.get("architecture") or {}).get("modality","")
        if drop.search(mid): continue
        if (m.get("capabilities") or {}).get("image_to_image") or keep.search(mod) or hint.search(mid+" "+(m.get("description") or "")):
            out.append(mid)
    return out
cands = candidates()
print("testing", len(cands), "models")
with ThreadPoolExecutor(max_workers=6) as ex:
    res = list(ex.map(call, cands))
res.sort(key=lambda r: (not r.get("honors"), r.get("out",999)))
json.dump(res, open(os.path.join(OUT,"batch_results.json"),"w"), indent=1)
print("\n=== HONORS MASK (out<20, in>12) ===")
for r in res:
    if r.get("honors"): print(f"  {'~weak' if r['weak'] else '  OK '} {r['model']:<48} in={r['in']:<6} out={r['out']:<5} ratio={r['ratio']}")
print("\n=== ignores mask / errored ===")
for r in res:
    if not r.get("honors"):
        print(f"   {r['model']:<48} "+(r['err'] if not r['ok'] else f"in={r['in']} out={r['out']} (mask ignored)"))
