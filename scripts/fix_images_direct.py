"""
Third-pass: directly download images for the 13 remaining recipes
using curated, known-good image URLs from food photography sites.
No API needed — direct HTTPS downloads.
"""
import os
import sys
from pathlib import Path
from tempfile import NamedTemporaryFile

sys.path.insert(0, str(Path(__file__).parent.parent))

import requests
from PIL import Image

STATIC_IMG_DIR = Path(__file__).parent.parent / 'static' / 'images' / 'recipes'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122 Safari/537.36',
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'Referer': 'https://www.google.com/',
}

# Curated direct image URLs (Unsplash, reputable food photo CDNs — free to use)
DIRECT_URLS = {
    18:  ('Perfect Fluffy Pancakes',    [
        'https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=900',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Pancakes_with_blueberries.jpg/1280px-Pancakes_with_blueberries.jpg',
    ]),
    19:  ('Molten Chocolate Lava Cake', [
        'https://images.unsplash.com/photo-1624353365286-3f8d62daad51?w=900',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Volcanocake.jpg/1280px-Volcanocake.jpg',
    ]),
    1:   ('Authentic Mutton Biryani',   [
        'https://images.unsplash.com/photo-1631515243349-e0cb75fb8d3a?w=900',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Biryani_at_Darbar.jpg/1280px-Biryani_at_Darbar.jpg',
    ]),
    294: ('Mixed Veg Curry',            [
        'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=900',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Dal_makhani.jpg/1280px-Dal_makhani.jpg',
    ]),
    281: ('Paneer Biryani',             [
        'https://images.unsplash.com/photo-1603360946369-dc9bb6258143?w=900',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Biryani_at_Darbar.jpg/800px-Biryani_at_Darbar.jpg',
    ]),
    387: ('Tofu Green Curry',           [
        'https://images.unsplash.com/photo-1455619452474-d2be8b1e70cd?w=900',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Tom_Kha_Gai_by_kazzbr.jpg/1280px-Tom_Kha_Gai_by_kazzbr.jpg',
    ]),
    17:  ('Authentic Pad Thai',         [
        'https://images.unsplash.com/photo-1516100882582-96c3a05fe590?w=900',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Phad_thai_kung_chang_kien.jpg/1280px-Phad_thai_kung_chang_kien.jpg',
    ]),
    333: ('Kani Salad',                 [
        'https://images.unsplash.com/photo-1607532941433-304659e8198a?w=900',
    ]),
    282: ('Mapo Tofu',                  [
        'https://images.unsplash.com/photo-1566506825668-4b1e3f25f8b1?w=900',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Chen_Mapo_Tofu.jpg/1280px-Chen_Mapo_Tofu.jpg',
    ]),
    215: ('Shrimp Scampi',              [
        'https://images.unsplash.com/photo-1603360946369-dc9bb6258143?w=900',
    ]),
    232: ('Crab Masala',                [
        'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=900',
    ]),
    334: ('Crab Stuffed Mushrooms',     [
        'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=900',
    ]),
    414: ('Tacos al Pastor',            [
        'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=900',
        'https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/001_Tacos_de_carnitas%2C_calle_Marzano%2C_col._Portales%2C_CDMX.jpg/1280px-001_Tacos_de_carnitas%2C_calle_Marzano%2C_col._Portales%2C_CDMX.jpg',
    ]),
}


def save_from_url(url, rid, name):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()

        tmp = NamedTemporaryFile(delete=False, suffix='.tmp')
        tmp.write(resp.content)
        tmp.close()

        img = Image.open(tmp.name)
        if img.width < 200 or img.height < 150:
            os.unlink(tmp.name)
            return False
        if img.mode in ('RGBA', 'P', 'LA'):
            img = img.convert('RGB')

        out = STATIC_IMG_DIR / f"{rid}.jpg"
        img.save(out, 'JPEG', quality=87, optimize=True)
        os.unlink(tmp.name)
        print(f"[{rid}] OK  {name}  ({img.width}x{img.height})", flush=True)
        return True
    except Exception as e:
        print(f"[{rid}] FAIL {url[:60]}: {e}", flush=True)
        return False


def main():
    ok = 0
    for rid, (name, urls) in DIRECT_URLS.items():
        print(f"\n[{rid}] {name}", flush=True)
        success = False
        for url in urls:
            if save_from_url(url, rid, name):
                ok += 1
                success = True
                break
        if not success:
            print(f"[{rid}] FAIL - all URLs failed for {name}", flush=True)

    print(f"\nDone: {ok}/{len(DIRECT_URLS)} images saved.", flush=True)


if __name__ == '__main__':
    main()
