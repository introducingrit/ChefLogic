"""
Targeted image re-download for recipes with confirmed wrong/bad images.
Uses very specific search queries per dish to ensure correct images.
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
STATIC_IMG_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/121 Safari/537.36',
    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
}

# recipe_id -> (recipe name, VERY SPECIFIC search query)
TARGETS = {
    18:  ('Perfect Fluffy Pancakes',      'fluffy pancakes stack breakfast food'),
    19:  ('Molten Chocolate Lava Cake',   'molten chocolate lava cake dessert food'),
    327: ('Honey Walnut Shrimp',          'honey walnut shrimp chinese dish food'),
    490: ('Gulab Jamun',                  'gulab jamun indian sweet dessert food'),
    1:   ('Authentic Mutton Biryani',     'mutton biryani rice dish food authentic'),
    202: ('Mutton Biryani',               'mutton biryani rice hyderabadi food'),
    220: ('Prawn Biryani',                'prawn biryani seafood rice dish food'),
    294: ('Mixed Veg Curry',              'mixed vegetable curry indian food'),
    281: ('Paneer Biryani',               'paneer biryani vegetarian rice dish'),
    264: ('Chicken Curry',                'chicken curry indian gravy food dish'),
    337: ('Blue Crab Curry',              'blue crab curry seafood dish food'),
    387: ('Tofu Green Curry',             'tofu green curry thai food dish'),
    17:  ('Authentic Pad Thai',           'pad thai noodles thailand food dish'),
    225: ('Crab Curry',                   'crab curry seafood indian food'),
    238: ('Roast Lamb',                   'roast lamb dinner sunday food'),
    336: ('Crab Pasta',                   'crab pasta seafood italian food'),
    289: ('Tofu Scramble',                'tofu scramble vegan breakfast food'),
    302: ('Salad varieties',              'mixed salad bowl varieties food'),
    333: ('Kani Salad',                   'kani salad japanese crab stick food'),
    282: ('Mapo Tofu',                    'mapo tofu sichuan chinese dish food'),
    215: ('Shrimp Scampi',                'shrimp scampi pasta garlic butter food'),
    232: ('Crab Masala',                  'crab masala indian spicy seafood curry'),
    334: ('Crab Stuffed Mushrooms',       'crab stuffed mushrooms appetizer food'),
    335: ('Dungeness Crab Boil',          'dungeness crab boil seafood food'),
    422: ('Fish and Chips',               'fish and chips british pub food'),
    277: ('Paneer Bhurji',                'paneer bhurji scrambled cottage cheese indian'),
    376: ('Paneer Lababdar',              'paneer lababdar rich tomato gravy indian food'),
    377: ('Paneer Kali Mirch',            'paneer kali mirch black pepper curry food'),
    378: ('Paneer Makhani Pizza',         'paneer makhani pizza indian fusion food'),
    388: ('Tofu Teriyaki Bowl',           'tofu teriyaki bowl japanese food'),
    209: ('Kebabs',                       'mixed kebab skewers grilled food'),
    414: ('Tacos al Pastor',              'tacos al pastor mexican street food'),
    352: ('Pork Ramen',                   'pork ramen japanese noodle soup bowl food'),
    406: ('Ramen',                        'ramen japanese noodle soup broth bowl food'),
}


def get_ddgs_image(query: str, retries: int = 2):
    for attempt in range(retries + 1):
        try:
            with DDGS() as ddgs:
                results = list(ddgs.images(query, max_results=6))
            for r in results:
                url = r.get('image', '')
                # Prefer jpg/jpeg/png, skip SVG/tiny images
                if (url and url.startswith('http')
                        and not url.endswith('.svg')
                        and not url.endswith('.gif')):
                    return url
        except Exception as e:
            if attempt < retries:
                time.sleep(3)
            else:
                print(f"  DDG error after {retries+1} tries: {e}", flush=True)
    return None


def download_image(url: str, rid: int, name: str) -> bool:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()

        # Validate it's actually an image
        content_type = resp.headers.get('content-type', '')
        if 'image' not in content_type and len(resp.content) < 5000:
            print(f"[{rid}] SKIP - not a valid image ({content_type})", flush=True)
            return False

        tmp = NamedTemporaryFile(delete=False, suffix='.tmp')
        tmp.write(resp.content)
        tmp.close()

        img = Image.open(tmp.name)
        # Minimum size check - reject tiny/icon images
        if img.width < 200 or img.height < 150:
            print(f"[{rid}] SKIP - too small ({img.width}x{img.height})", flush=True)
            os.unlink(tmp.name)
            return False

        if img.mode in ('RGBA', 'P', 'LA'):
            img = img.convert('RGB')

        out_path = STATIC_IMG_DIR / f"{rid}.jpg"
        img.save(out_path, 'JPEG', quality=87, optimize=True)
        os.unlink(tmp.name)
        print(f"[{rid}] OK - {name} ({img.width}x{img.height})", flush=True)
        return True
    except Exception as e:
        print(f"[{rid}] FAIL download {name}: {e}", flush=True)
        try:
            if os.path.exists(tmp.name):
                os.unlink(tmp.name)
        except Exception:
            pass
        return False


def main():
    ok_count = 0
    fail_list = []
    total = len(TARGETS)

    for i, (rid, (name, query)) in enumerate(TARGETS.items()):
        print(f"\n[{i+1}/{total}] {name} (ID {rid})", flush=True)
        print(f"  Query: {query}", flush=True)

        # Try up to 3 different URLs from DDG results
        url = get_ddgs_image(query)
        if url:
            success = download_image(url, rid, name)
            if success:
                ok_count += 1
            else:
                # Try a fallback URL with a slightly different query
                url2 = get_ddgs_image(name + ' food recipe plated')
                if url2 and url2 != url:
                    if download_image(url2, rid, name):
                        ok_count += 1
                    else:
                        fail_list.append((rid, name))
                else:
                    fail_list.append((rid, name))
        else:
            fail_list.append((rid, name))

        # Delay between requests to avoid rate limiting
        if i < total - 1:
            time.sleep(2.5)

    print(f"\n{'='*50}", flush=True)
    print(f"Done. {ok_count}/{total} images updated.", flush=True)
    if fail_list:
        print("Failed:", flush=True)
        for rid, name in fail_list:
            print(f"  [{rid}] {name}", flush=True)


if __name__ == '__main__':
    main()
