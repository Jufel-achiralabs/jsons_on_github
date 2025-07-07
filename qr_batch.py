#!/usr/bin/env python3
"""
qr_batch.py – emit PNGs for every *.json in ./data
pip install qrcode[pil] tqdm
"""
from pathlib import Path
import qrcode, tqdm, subprocess, os

BASE_URL = "https://cdn.jsdelivr.net/gh/jufel-achiralabs/jsons_on_github@master"  # pin later if you tag
BASE_PATH = r"D:\Jufel\repos\jsons_on_github"

for p in tqdm.tqdm(list(Path("data").rglob("*.json"))):
    url = f"{BASE_URL}/{p.as_posix()}"
    print(url)
    out = Path("qr") / p.with_suffix(".png").name
    print(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    qrcode.make(url).save(out)
