#!/usr/bin/env python3
# scripts/generate_index.py
import json, glob, os, datetime
from dateutil import parser as dateparser

CLIPS_DIR = "clips"
OUT_FILE = os.path.join(CLIPS_DIR, "index.json")

def load_clip(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    files = sorted(glob.glob(os.path.join(CLIPS_DIR, "*.json")))
    clips = []
    for f in files:
        if f.endswith("index.json"):
            continue
        try:
            c = load_clip(f)
            clips.append(c)
        except Exception as e:
            print("skip", f, e)
    # sort by upload_date if present
    def keyfn(x):
        try:
            return dateparser.parse(x.get("upload_date"))
        except Exception:
            return datetime.datetime.min
    clips.sort(key=keyfn, reverse=True)
    out = {"generated_at": datetime.datetime.utcnow().isoformat() + "Z", "count": len(clips), "clips": clips}
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("Wrote", OUT_FILE, "with", len(clips), "clips")

if __name__ == "__main__":
    main()
