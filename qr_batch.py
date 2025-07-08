#!/usr/bin/env python3
"""
qr_batch.py - emit PNGs for every *.json in ./data
pip install qrcode[pil] tqdm
"""
from pathlib import Path
import qrcode, tqdm, json, subprocess, os
import requests


BASE_URL = "https://cdn.jsdelivr.net/gh/jufel-achiralabs/jsons_on_github@master"  # pin later if you tag
DATA_DIR = Path("data")
QR_DIR   = Path("qr")
MANIFEST_PATH = Path("short_urls.json")

# Load old manifest if it exists (to avoid re-shortening same links)
if MANIFEST_PATH.exists():
    with open(MANIFEST_PATH, "r") as f:
        manifest = json.load(f)
else:
    manifest = {}

def shorten_url(long_url: str) -> str:
    api = "https://tinyurl.com/api-create.php"
    try:
        resp = requests.get(api, params={"url": long_url}, timeout=5)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print("❌ Failed to shorten URL:", e)
        return long_url  # fallback to original

all_jsons = list(DATA_DIR.rglob("*.json"))
print(f"Found {len(all_jsons)} jsons.")

for json_file in tqdm.tqdm(all_jsons):
    # # Relative path inside 'data/' → like 0000-0999/foo.json
    # rel_path = json_file.relative_to(DATA_DIR)
    # print(json_file)

    # url = f"{BASE_URL}/{json_file.as_posix()}"
    # print(url)

    # out = QR_DIR / rel_path.with_suffix(".png")
    # print(out)
    # out.parent.mkdir(parents=True, exist_ok=True)
    # qrcode.make(url).save(out)

    rel_path = json_file.relative_to(DATA_DIR)
    key = str(rel_path).replace("\\", "/")  # normalize for manifest keys

    print("📄 JSON:", json_file)

    long_url = f"{BASE_URL}/data/{key}"
    print("🔗 Long URL:", long_url)

    # Use previously shortened URL if available
    if key in manifest:
        short_url = manifest[key]["short_url"]
    else:
        short_url = shorten_url(long_url)
        manifest[key] = {
            "original_url": long_url,
            "short_url": short_url
        }

    out = QR_DIR / rel_path.with_suffix(".png")
    print("🖼  QR Path:", out)
    out.parent.mkdir(parents=True, exist_ok=True)

    qr = qrcode.QRCode(
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=2,
        border=2
    )
    qr.add_data(short_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(out)

    # Add qr_path to manifest
    manifest[key]["qr_path"] = str(out)

# Save the updated manifest
with open(MANIFEST_PATH, "w") as f:
    json.dump(manifest, f, indent=2)

print(f"\n✅ Done: {len(all_jsons)} files processed")
print(f"📄 Manifest saved to {MANIFEST_PATH}")