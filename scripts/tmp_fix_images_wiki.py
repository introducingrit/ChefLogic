import os
import time
from pathlib import Path
from tempfile import NamedTemporaryFile
import requests
import pandas as pd
from PIL import Image

PROCESSED_DATA_PATH = Path('c:/Users/RITAJA/Downloads/ChefLogic/data/processed/recipes_clean.csv')
STATIC_IMG_DIR = Path('c:/Users/RITAJA/Downloads/ChefLogic/static/images/recipes')

HEADERS = {
    'User-Agent': 'ChefLogicBot/1.0 (https://cheflogic.example.com; contact@cheflogic.com)',
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
    # Use Wikimedia Commons / Wikipedia API
    # gsrsearch gets the article, pageimages gets the image
    url = f"https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&generator=search&gsrsearch={requests.utils.quote(dish_name + ' food plate')}&gsrlimit=2"
    
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        data = r.json()
        pages = data.get('query', {}).get('pages', {})
        
        # return the first valid original image URL
        for p in pages.values():
            img_url = p.get('original', {}).get('source')
            if img_url and img_url.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                # Filter out standard wikipedia icons
                if 'Ambox' not in img_url and 'Wikidata' not in img_url:
                    return img_url
                    
        # Fallback simpler search
        fallback_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&generator=search&gsrsearch={requests.utils.quote(dish_name)}&gsrlimit=2"
        data = requests.get(fallback_url, headers=HEADERS, timeout=10).json()
        pages = data.get('query', {}).get('pages', {})
        for p in pages.values():
            img_url = p.get('original', {}).get('source')
            if img_url and img_url.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                if 'Ambox' not in img_url and 'Wikidata' not in img_url:
                    return img_url
                    
    except Exception as e:
        print(f"  Wiki API Error: {e}", flush=True)
        
    return None

def download_and_save(rid: int, name: str) -> bool:
    print(f"[{rid}] Searching Wiki for: {name} ...", flush=True)
    url = get_image_url(name)
    if not url:
        print(f"[{rid}] FAIL - no Wiki image for {name}", flush=True)
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
        print(f"[{rid}] OK - saved {url.split('/')[-1]}", flush=True)
        return True
    except Exception as e:
        print(f"[{rid}] FAIL: {name}: {e}\nURL: {url}", flush=True)
        return False

def main():
    if not PROCESSED_DATA_PATH.exists():
        print("Dataset not found!", flush=True)
        return

    df = pd.read_csv(PROCESSED_DATA_PATH)
    names_lower = [n.lower() for n in RECIPES_TO_FIX]
    
    to_update = []
    for _, row in df.iterrows():
        try:
            name = str(row['name'])
            if name.lower() in names_lower:
                to_update.append((int(row['id']), name))
        except Exception:
            continue

    print(f"Found {len(to_update)} recipes.")

    ok = 0
    for i, (rid, name) in enumerate(to_update):
        # We can optimize: don't re-download if we already got it using DDG in last 5 mins
        # but the prompt says update them. Let's just update all matching ones so we are 100% sure.
        if download_and_save(rid, name):
            ok += 1
        time.sleep(1) # Wikipedia limits are very generous, 1s is perfectly safe

    print(f"\nDone. {ok}/{len(to_update)} images updated from Wikipedia.", flush=True)

if __name__ == '__main__':
    main()
