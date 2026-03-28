"""Fix missing images using ddgs image search with longer delays to avoid rate limiting."""
import os
import sys
import time
from pathlib import Path
from tempfile import NamedTemporaryFile

sys.path.insert(0, str(Path(__file__).parent.parent))

import requests
import pandas as pd
from PIL import Image
from ddgs import DDGS

PROCESSED_DATA_PATH = Path(__file__).parent.parent / 'data' / 'processed' / 'recipes_clean.csv'
STATIC_IMG_DIR = Path(__file__).parent.parent / 'static' / 'images' / 'recipes'
STATIC_IMG_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36',
}

# Only download ones still missing
MISSING_IDS = [246, 257, 264, 281, 282, 310, 317, 370, 377, 379, 384,
               403, 412, 438, 440, 490, 492, 496, 497]  # 501, 510 already done


def get_image_url(dish_name: str):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.images(
                f"{dish_name} food dish recipe",
                max_results=4,
            ))
        for r in results:
            url = r.get('image', '')
            if url and url.startswith('http') and not url.endswith('.svg'):
                return url
    except Exception as e:
        print(f"  DDG error: {e}", flush=True)
    return None


def download_and_save(rid: int, name: str) -> bool:
    print(f"[{rid}] Downloading: {name} ...", flush=True)
    url = get_image_url(name)
    if not url:
        print(f"[{rid}] FAIL - no DDG image for {name}", flush=True)
        return False

    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()

        tmp = NamedTemporaryFile(delete=False, suffix='.tmp')
        tmp.write(resp.content)
        tmp.close()

        img = Image.open(tmp.name)
        if img.mode in ('RGBA', 'P', 'LA'):
            img = img.convert('RGB')

        out_path = STATIC_IMG_DIR / f"{rid}.jpg"
        img.save(out_path, 'JPEG', quality=85)
        os.unlink(tmp.name)
        print(f"[{rid}] OK - {name}", flush=True)
        return True
    except Exception as e:
        print(f"[{rid}] FAIL: {name}: {e}", flush=True)
        return False


def main():
    if not PROCESSED_DATA_PATH.exists():
        print("Dataset not found!", flush=True)
        return

    df = pd.read_csv(PROCESSED_DATA_PATH)
    id_to_name = {}
    for _, row in df.iterrows():
        try:
            id_to_name[int(row['id'])] = row['name']
        except Exception:
            pass

    ok = 0
    for i, rid in enumerate(MISSING_IDS):
        jpg = STATIC_IMG_DIR / f"{rid}.jpg"
        png = STATIC_IMG_DIR / f"{rid}.png"
        if jpg.exists() or png.exists():
            print(f"[{rid}] Already exists, skipping.", flush=True)
            ok += 1
            continue
        name = id_to_name.get(rid, '')
        if not name:
            print(f"[{rid}] ID not found.", flush=True)
            continue

        if download_and_save(rid, name):
            ok += 1

        # Wait 4 seconds between each request to avoid DDG rate limiting
        if i < len(MISSING_IDS) - 1:
            time.sleep(4)

    print(f"\nDone. {ok}/{len(MISSING_IDS)} images ready.", flush=True)


if __name__ == '__main__':
    main()
