#!/usr/bin/env python3
import os, sys, json, uuid, shutil
from datetime import datetime

CLIPS_DIR = "clips"  # donde se guardan todos los videos y metadatos

def ask_input(prompt, default=None):
    val = input(prompt)
    if not val.strip() and default is not None:
        return default
    return val.strip()

def main():
    print("=== Ro-Leak Upload Tool ===")
    title = ask_input("Title: ")
    description = ask_input("Description: ")
    tags = ask_input("Tags (comma-separated): ").split(",")
    tags = [t.strip() for t in tags if t.strip()]
    video_path = ask_input("Path to video file: ")

    if not os.path.isfile(video_path):
        print("❌ Video file does not exist.")
        return

    # Generate unique ID
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    vid_id = f"{timestamp}_{uuid.uuid4().hex[:6]}"
    vid_folder = os.path.join(CLIPS_DIR, vid_id)
    os.makedirs(vid_folder, exist_ok=True)

    # Copy video
    video_filename = os.path.basename(video_path)
    dest_video_path = os.path.join(vid_folder, video_filename)
    shutil.copy2(video_path, dest_video_path)

    # Generate metadata.json
    metadata = {
        "id": vid_id,
        "title": title,
        "description": description,
        "tags": tags,
        "upload_date": datetime.utcnow().isoformat() + "Z",
        "video_file": video_filename
    }
    metadata_path = os.path.join(vid_folder, "metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    print(f"✅ Video saved in {vid_folder}")
    print(f"✅ Metadata saved in {metadata_path}")

if __name__ == "__main__":
    os.makedirs(CLIPS_DIR, exist_ok=True)
    main()
