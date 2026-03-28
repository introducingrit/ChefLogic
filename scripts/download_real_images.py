import os
import sys
import pandas as pd
import requests
from pathlib import Path
from tempfile import NamedTemporaryFile
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import PROCESSED_DATA_PATH

STATIC_IMG_DIR = Path(__file__).resolve().parents[1] / 'static' / 'images' / 'recipes'
STATIC_IMG_DIR.mkdir(parents=True, exist_ok=True)

def get_wiki_image(dish_name):
    headers = {'User-Agent': 'ChefLogic/1.0 (contact@example.com)'}
    try:
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={dish_name} food&utf8=&format=json"
        res = requests.get(search_url, headers=headers, timeout=5).json()
        if not res.get('query', {}).get('search'):
            return None
        title = res['query']['search'][0]['title']
        
        img_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={title}&prop=pageimages&format=json&pithumbsize=1000"
        img_res = requests.get(img_url, headers=headers, timeout=5).json()
        pages = img_res.get('query', {}).get('pages', {})
        for page_id in pages:
            if 'thumbnail' in pages[page_id]:
                return pages[page_id]['thumbnail']['source']
    except Exception as e:
        print(f"Wiki fetch err: {e}", flush=True)
    return None

def download_images():
    if not os.path.exists(PROCESSED_DATA_PATH):
        print("Dataset not found!", flush=True)
        return

    df = pd.read_csv(PROCESSED_DATA_PATH)
    df_new = df[df['id'] >= 201]

    headers = {'User-Agent': 'ChefLogic/1.0'}
    
    for _, row in df_new.iterrows():
        rid = row['id']
        name = row['name']
        
        existing = list(STATIC_IMG_DIR.glob(f"{rid}.*"))
        if existing:
            # Skip only if we have a real image? Actually, let's skip if it exists
            print(f"[{rid}] Image already exists for {name}, skipping.", flush=True)
            continue
            
        print(f"[{rid}] Searching Wikipedia for: {name}...", flush=True)
        url = get_wiki_image(name)
        
        if not url:
            print(f"[{rid}] No Wikipedia image found for {name}.", flush=True)
            continue
            
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            
            temp = NamedTemporaryFile(delete=False)
            temp.write(resp.content)
            temp.close()
            
            try:
                img = Image.open(temp.name)
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                    
                final_path = STATIC_IMG_DIR / f"{rid}.jpg"
                img.save(final_path, "JPEG", quality=85)
                print(f"[{rid}] Successfully downloaded and saved {name} as JPG.", flush=True)
            except Exception as e:
                print(f"[{rid}] Failed to process image for {name}: {e}", flush=True)
                
            os.unlink(temp.name)
                
        except Exception as e:
            print(f"[{rid}] Download failed for {name}: {e}", flush=True)

if __name__ == "__main__":
    download_images()
