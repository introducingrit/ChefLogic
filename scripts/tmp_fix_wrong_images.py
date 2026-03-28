import os
import time
from pathlib import Path
from tempfile import NamedTemporaryFile
import requests
import pandas as pd
from PIL import Image
from ddgs import DDGS

PROCESSED_DATA_PATH = Path('c:/Users/RITAJA/Downloads/ChefLogic/data/processed/recipes_clean.csv')
STATIC_IMG_DIR = Path('c:/Users/RITAJA/Downloads/ChefLogic/static/images/recipes')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36',
}

RECIPES_TO_FIX = [
    "Zucchini Fritters", "Vegetable Tempura", "Veg Sushi", "Veg Lasagna", "Udon", 
    "Tofu Summer Rolls", "Vegetable Stir Fry", "Soft Shell Crab Tempura", "Soba Noodles", 
    "Quinoa Salad", "Pulled Pork", "Prawn Curry", "Prawn Balchão", "Pork Dumplings", 
    "Pork Belly", "Noodles", "Mutton Sukka", "Mochi", "Meatballs", "Lechon", 
    "Lamb Shank Braised", "Lamb Chops", "Kharahi Gosht", "Kedgeree", "Jeera Rice", 
    "Hot Dog", "Halloumi Grill", "Fried Chicken", "Fish And Chips", "Donuts", 
    "Chicken Marbella", "Chicken Adobo", "Cabrito Asado", "Bulgur Pilaf", "Bbq Platters", 
    "Arroz Con Pollo", "Adobo Pork"
]

def get_image_url(dish_name: str):
    try:
        with DDGS() as ddgs:
            # use a simpler query so duckduckgo actually returns results
            results = list(ddgs.images(
                f"{dish_name} meal plate hi res",
                max_results=5,
            ))
        
        # We will try to pick the second or third image to ensure it's different 
        # from whatever the original script fetched (which probably picked the 1st)
        valid_urls = []
        for r in results:
            url = r.get('image', '')
            if url and url.startswith('http') and not url.endswith('.svg') and 'youtube' not in url.lower():
                valid_urls.append(url)
        
        if len(valid_urls) > 1:
            return valid_urls[1] # Pick the 2nd one to avoid repeating the mistake
        elif valid_urls:
            return valid_urls[0]
            
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
        resp = requests.get(url, headers=HEADERS, timeout=12)
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
        print(f"[{rid}] OK - saved {url}", flush=True)
        return True
    except Exception as e:
        print(f"[{rid}] FAIL: {name}: {e}\nURL: {url}", flush=True)
        return False

def main():
    if not PROCESSED_DATA_PATH.exists():
        print("Dataset not found!", flush=True)
        return

    df = pd.read_csv(PROCESSED_DATA_PATH)
    
    # Map lowercase requested names to IDs
    names_lower = [n.lower() for n in RECIPES_TO_FIX]
    
    to_update = []
    for _, row in df.iterrows():
        try:
            name = str(row['name'])
            if name.lower() in names_lower:
                to_update.append((int(row['id']), name))
        except Exception:
            continue

    print(f"Found {len(to_update)} / {len(RECIPES_TO_FIX)} matching recipes in DB.")

    ok = 0
    for i, (rid, name) in enumerate(to_update):
        if download_and_save(rid, name):
            ok += 1
        # Delay to avoid rate limits
        if i < len(to_update) - 1:
            time.sleep(3)

    print(f"\nDone. {ok}/{len(to_update)} images updated.", flush=True)

if __name__ == '__main__':
    main()
