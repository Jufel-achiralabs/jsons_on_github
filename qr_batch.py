#!/usr/bin/env python3
"""
qr_batch.py – emit PNGs for every *.json in ./data
pip install qrcode[pil] tqdm
"""
from pathlib import Path
import qrcode, tqdm, subprocess, os

BASE_URL = "https://cdn.jsdelivr.net/gh/jufel-achiralabs/jsons_on_github@master"  # pin later if you tag
DATA_DIR = Path("data")
QR_DIR   = Path("qr")

all_jsons = list(DATA_DIR.rglob("*.json"))

for json_file in tqdm.tqdm(all_jsons):
    # Relative path inside 'data/' → like 0000-0999/foo.json
    rel_path = json_file.relative_to(DATA_DIR)
    print(rel_path)
    url = f"{BASE_URL}/{rel_path.as_posix()}"
    print(url)
    out = QR_DIR / rel_path.with_suffix(".png")
    print(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    qrcode.make(url).save(out)
