"""
Second pass: re-download the 13 images that failed in the first run.
Longer delays to avoid DDG rate limiting.
Uses alternative, shorter search terms.
"""
import os
import sys
import time
from pathlib import Path
from tempfile import NamedTemporaryFile

sys.path.insert(0, str(Path(__file__).parent.parent))

import requests
from PIL import Image
from ddgs import DDGS

STATIC_IMG_DIR = Path(__file__).parent.parent / 'static' / 'images' / 'recipes'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122 Safari/537.36',
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
}

# Shorter, simpler queries that DDG finds more reliably
TARGETS_RETRY = {
    18:  ('Perfect Fluffy Pancakes',  ['fluffy pancakes breakfast', 'american pancakes stack maple syrup']),
    19:  ('Molten Chocolate Lava Cake',['chocolate lava cake dessert', 'fondant au chocolat cake']),
    1:   ('Authentic Mutton Biryani', ['mutton biryani', 'hyderabadi biryani rice']),
    294: ('Mixed Veg Curry',          ['vegetable curry indian', 'mixed veg curry cooking']),
    281: ('Paneer Biryani',           ['paneer biryani', 'veg biryani paneer rice']),
    387: ('Tofu Green Curry',         ['green curry tofu', 'thai green curry tofu bowl']),
    17:  ('Authentic Pad Thai',       ['pad thai noodles', 'pad thai thai food recipe']),
    333: ('Kani Salad',               ['kani salad', 'japanese crab stick salad']),
    282: ('Mapo Tofu',                ['mapo tofu', 'mapo doufu sichuan spicy tofu']),
    215: ('Shrimp Scampi',            ['shrimp scampi', 'scampi pasta garlic white wine']),
    232: ('Crab Masala',              ['crab masala curry', 'crab curry masala indian spicy']),
    334: ('Crab Stuffed Mushrooms',   ['stuffed mushrooms crab', 'crab stuffed mushrooms baked']),
    414: ('Tacos al Pastor',          ['tacos al pastor', 'taco al pastor mexican pork']),
}


def get_image_url(queries: list):
    for q in queries:
        try:
            with DDGS() as ddgs:
                results = list(ddgs.images(q, max_results=5))
            for r in results:
                url = r.get('image', '')
                if url and url.startswith('http') and not url.endswith('.svg'):
                    return url
        except Exception as e:
            print(f"  DDG query '{q}' error: {e}", flush=True)
        time.sleep(4)
    return None


def save_image(url, rid, name):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()

        tmp = NamedTemporaryFile(delete=False, suffix='.tmp')
        tmp.write(resp.content)
        tmp.close()

        img = Image.open(tmp.name)
        if img.width < 200 or img.height < 150:
            os.unlink(tmp.name)
            print(f"[{rid}] SKIP too small ({img.width}x{img.height})", flush=True)
            return False

        if img.mode in ('RGBA', 'P', 'LA'):
            img = img.convert('RGB')

        out = STATIC_IMG_DIR / f"{rid}.jpg"
        img.save(out, 'JPEG', quality=87, optimize=True)
        os.unlink(tmp.name)
        print(f"[{rid}] OK  {name}  ({img.width}x{img.height})", flush=True)
        return True
    except Exception as e:
        print(f"[{rid}] FAIL {name}: {e}", flush=True)
        return False


def main():
    ok = 0
    total = len(TARGETS_RETRY)
    for i, (rid, (name, queries)) in enumerate(TARGETS_RETRY.items()):
        print(f"\n[{i+1}/{total}] {name}", flush=True)
        url = get_image_url(queries)
        if url:
            if save_image(url, rid, name):
                ok += 1
            else:
                print(f"[{rid}] FAIL to save", flush=True)
        else:
            print(f"[{rid}] FAIL no image found", flush=True)
        # Long pause between recipes
        if i < total - 1:
            time.sleep(5)

    print(f"\nDone: {ok}/{total} rescued.", flush=True)


if __name__ == '__main__':
    main()
