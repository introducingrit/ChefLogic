"""
Script to generate placeholder PNG images for recipe IDs.
Creates simple images with the recipe name displayed.
"""
import os
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    raise ImportError('Pillow is required to run this script. Install via pip install pillow')

# Directory to save images
STATIC_IMG_DIR = Path(__file__).resolve().parents[1] / 'static' / 'images' / 'recipes'
STATIC_IMG_DIR.mkdir(parents=True, exist_ok=True)

# Load recipe data to get names
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.generate_sample_data import RECIPES

# Create images for each recipe ID
for rec in RECIPES:
    rid, name = rec[0], rec[1]
    img_path = STATIC_IMG_DIR / f"{rid}.png"
    if img_path.exists():
        continue  # skip if already exists
    # Create image
    img = Image.new('RGB', (400, 300), color=(240, 240, 240))
    draw = ImageDraw.Draw(img)
    # Use a basic font
    try:
        font = ImageFont.truetype('arial.ttf', 20)
    except Exception:
        font = ImageFont.load_default()
    text = name
    # Compute text size using textbbox for compatibility
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text(((400 - w) / 2, (300 - h) / 2), text, fill='black', font=font)
    img.save(img_path)
    print(f"Created placeholder image for recipe {rid}: {img_path}")
