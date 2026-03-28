import pandas as pd
import os
import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import PROCESSED_DATA_PATH

RAW_DATA = """
🐐 Mutton (Goat/Lamb in some regions)
Rogan Josh (India)
Mutton Biryani (South Asia)
Nihari (Pakistan/India)
Mutton Korma
Mutton Curry
Shepherd’s Pie (UK, often lamb)
Moussaka (Greece)
Lamb Tagine (Morocco)
Kebabs (Middle East – Seekh, Shish)
Lamb Chops (global)
Haggis (Scotland)
Lamb Shawarma
🦐 Prawn (Shrimp)
Prawn Curry (India, Thailand)
Garlic Butter Shrimp
Shrimp Scampi (Italy/US)
Tempura Shrimp (Japan)
Kung Pao Shrimp (China)
Shrimp Fried Rice
Shrimp Tacos (Mexico)
Prawn Biryani
Tom Yum Goong (Thailand)
Jambalaya (USA)
Shrimp Etouffee (Louisiana)
🦀 Crab
Chilli Crab (Singapore)
Crab Curry (India)
Soft Shell Crab Tempura (Japan)
Crab Cakes (USA)
Crab Rangoon (Chinese-American)
Singapore Black Pepper Crab
Maryland Crab Soup
Crab Fried Rice
Crab Masala
🐑 Lamb (distinct category globally)
Lamb Biryani
Lamb Rogan Josh
Lamb Gyros (Greece)
Lamb Kofta
Lamb Stew
Roast Lamb (UK/Australia)
Lamb Tagine
Lamb Vindaloo (India)
Lamb Kebabs
🐖 Pork
Pork Belly (Korea – Samgyeopsal)
Sweet and Sour Pork (China)
Char Siu (Chinese BBQ pork)
Pork Vindaloo (Goa, India)
Bacon-based dishes
Pork Schnitzel (Germany)
Lechon (Philippines)
Tonkatsu (Japan)
Pulled Pork (USA)
Pork Dumplings
🐄 Beef
Beef Steak
Beef Stroganoff (Russia)
Beef Bourguignon (France)
Beef Tacos (Mexico)
Hamburger (USA)
Meatballs (global variations)
Beef Rendang (Indonesia)
Bulgogi (Korea)
Beef Pho (Vietnam)
Beef Curry (India)
🐔 Chicken
Butter Chicken (India)
Chicken Biryani
Chicken Curry (global)
Fried Chicken (USA/Korea)
Chicken Tikka
Chicken Alfredo Pasta (Italy/US)
Chicken Teriyaki (Japan)
Chicken Shawarma
Coq au Vin (France)
Chicken Satay (Indonesia)
Chicken Noodle Soup
🧀 Paneer (Indian vegetarian protein)
Paneer Butter Masala
Palak Paneer
Paneer Tikka
Shahi Paneer
Paneer Bhurji
Kadai Paneer
Malai Kofta
Paneer Pakora
Paneer Biryani
🟩 Tofu
Mapo Tofu (China)
Agedashi Tofu (Japan)
Tofu Stir Fry
Tofu Curry
Tofu Pad Thai (Thailand)
Miso Soup with Tofu (Japan)
Korean Sundubu Jjigae
Tofu Scramble (vegan)
🥦 Vegetables (Vegetarian/Vegan)
Vegetable Stir Fry (Asia)
Ratatouille (France)
Veg Biryani (India)
Aloo Gobi (India)
Mixed Veg Curry
Minestrone Soup (Italy)
Veg Sushi (Japan)
Falafel (Middle East)
Hummus
Stuffed Peppers
Veg Lasagna
Buddha Bowl
Salad varieties (global)
🍲 MIXED / COMBINATION DISHES
Paella (Spain – seafood/meat mix)
Jambalaya (USA)
Fried Rice (global variations)
Noodles (Asian cuisines)
Pizza (global toppings)
Pasta dishes
Hot Pot (China)
BBQ platters
🐐 MUTTON / GOAT (New dishes)
Laal Maas (India – Rajasthan)
Mutton Keema (minced curry, India)
Mutton Paya (trotter soup, South Asia)
Haleem (Middle East/South Asia)
Gosht Do Pyaza (India)
Mutton Sukka (South India)
Kharahi Gosht (Pakistan)
Mutton Yakhni (Kashmir)
Goat Pepper Soup (West Africa)
Cabrito Asado (Latin America – roasted goat)
🦐 PRAWN (New dishes)
Prawn Balchão (Goa, India)
Gambas al Ajillo (Spain)
Shrimp Po’ Boy (USA)
Shrimp Laksa (Malaysia)
Prawn Ceviche (Peru)
Shrimp Saganaki (Greece)
Honey Walnut Shrimp (China/US)
Prawn Okonomiyaki (Japan)
Shrimp Grits (Southern USA)
Prawn Sambal (Indonesia/Malaysia)
🦀 CRAB (New dishes)
Crab Thermidor (France)
Crab Laksa (Southeast Asia)
Kani Salad (Japan)
Crab Stuffed Mushrooms
Dungeness Crab Boil (USA)
Crab Pasta (Italy)
Blue Crab Curry (Sri Lanka)
Crab Omelette (Thailand – Kai Jeow Pu)
Deviled Crab (Caribbean)
🐑 LAMB (New dishes)
Lamb Navarin (France)
Lamb Shank Braised (global)
Lamb Pilaf (Central Asia)
Lamb Dolma (Middle East)
Lamb Souvlaki (Greece)
Lamb Harira (Morocco soup)
Lamb Saag (India)
Lamb Ribs BBQ
Lamb Fricassee (Mediterranean)
🐖 PORK (New dishes)
Adobo Pork (Philippines)
Pork Sisig (Philippines)
Feijoada (Brazil)
Pork Ramen (Japan)
Porchetta (Italy)
Pork Goulash (Hungary)
Carnitas (Mexico)
Pork Aspic (Eastern Europe)
Babi Guling (Indonesia)
🐄 BEEF (New dishes)
Carpaccio (Italy – raw beef)
Beef Tataki (Japan)
Beef Goulash (Hungary)
Beef Barbacoa (Mexico)
Beef Chili (USA)
Beef Kofta (Middle East)
Steak Tartare (France)
Beef Udon (Japan)
Beef Pepper Steak (China)
🐔 CHICKEN (New dishes)
Chicken Kiev (Ukraine)
Chicken Adobo (Philippines)
Chicken Paprikash (Hungary)
Chicken Marbella (Mediterranean)
Chicken Mole (Mexico)
Chicken Karaage (Japan)
Chicken Yassa (Senegal)
Chicken Cacciatore (Italy)
Chicken Empanadas (Latin America)
🧀 PANEER (New dishes)
Paneer Lababdar
Paneer Kali Mirch
Paneer Makhani Pizza (fusion)
Paneer Frankie (India street food)
Paneer Jalfrezi
Paneer Pasanda
Paneer Kathi Roll
Paneer Stuffed Paratha
Achari Paneer
🟩 TOFU (New dishes)
Tofu Katsu (Japan-style)
Tofu Banh Mi (Vietnam)
Tofu Green Curry (Thailand)
Tofu Teriyaki Bowl
Tofu Bibimbap (Korea)
Tofu Summer Rolls (Vietnam)
Tofu Noodle Soup
Grilled Tofu Skewers
Tofu Satay
🥦 VEGETABLE (New dishes)
Shakshuka (Middle East/North Africa)
Caponata (Italy)
Baingan Bharta (India)
Okra Gumbo (USA)
Vegetable Paella (Spain)
Kimchi (Korea)
Colcannon (Ireland)
Zucchini Fritters (Mediterranean)
Vegetable Tempura (Japan)
Stuffed Zucchini Boats
Eggplant Parmesan (Italy)
🍲 MORE MIXED / GLOBAL DISHES
Bibimbap (Korea)
Ramen (Japan)
Pho (Vietnam – variants)
Banh Mi (Vietnam sandwich)
Dumplings (China – jiaozi)
Pierogi (Poland)
Empanadas (Latin America)
Sushi Rolls (Japan varieties)
Burritos (Mexico)
Tacos al Pastor (Mexico)
Pasta Carbonara (Italy)
Risotto (Italy)
🐟 FISH (Seafood beyond prawn/crab)
Sushi Nigiri (Japan)
Sashimi (Japan)
Fish Amok (Cambodia)
Poke Bowl (Hawaii)
Gravlax (Scandinavia)
Fish and Chips (UK)
Moqueca (Brazil fish stew)
Bouillabaisse (France)
Escabeche Fish (Spain/Philippines)
Ikan Bakar (Indonesia grilled fish)
🥚 EGGS
Eggs Benedict (USA)
Shakshouka (Middle East – egg version differs regionally)
Tamago Sushi (Japan)
Spanish Tortilla (Spain)
Scotch Eggs (UK)
Menemen (Turkey)
Egg Drop Soup (China)
Frittata (Italy)
Omurice (Japan)
Huevos Rancheros (Mexico)
🍚 RICE-BASED DISHES
Risotto Milanese (Italy)
Arroz con Pollo (Latin America)
Tahdig (Iran crispy rice)
Kedgeree (UK/India fusion)
Nasi Lemak (Malaysia)
Nasi Goreng (Indonesia)
Jeera Rice (India)
Coconut Rice (tropical regions)
Claypot Rice (China)
Rice Congee (Asia)
🍝 GRAINS / NOODLES / BREAD
Udon (Japan)
Soba Noodles (Japan)
Couscous (North Africa)
Quinoa Salad (Peru/global)
Bulgur Pilaf (Middle East)
Spaghetti Aglio e Olio (Italy)
Mac and Cheese (USA)
Lasagna (Italy)
Roti / Chapati (India)
Injera (Ethiopia)
Pita Bread (Middle East)
🧀 CHEESE-BASED DISHES
Fondue (Switzerland)
Raclette (Switzerland/France)
Cheeseburger (USA)
Quesadilla (Mexico)
Halloumi Grill (Cyprus)
Cheese Soufflé (France)
Mozzarella Sticks
Cheese Omelette
Burrata Salad (Italy)
🍲 SOUPS & STEWS
Borscht (Ukraine)
Tom Kha Gai (Thailand)
Clam Chowder (USA)
Mulligatawny Soup (India/UK)
Minestra (Italy)
Lentil Soup (Middle East)
French Onion Soup
Gazpacho (Spain cold soup)
Pho Chay (Vietnam veg soup)
🍟 STREET FOOD / SNACKS
Hot Dog (USA)
Pretzel (Germany)
Corn Dog (USA/Korea)
Arepas (Venezuela/Colombia)
Samosa (India)
Spring Rolls (Asia)
Nachos (Mexico)
Falooda (India dessert drink)
Churros (Spain)
Takoyaki (Japan)
🍰 DESSERTS & SWEETS
Tiramisu (Italy)
Baklava (Turkey/Middle East)
Cheesecake (global)
Mochi (Japan)
Gulab Jamun (India)
Rasgulla (India)
Brownies (USA)
Pancakes (global)
Waffles (Belgium)
Donuts (USA)
Crème Brûlée (France)
🥗 SALADS & LIGHT DISHES
Caesar Salad (Italy/USA)
Greek Salad
Waldorf Salad (USA)
Coleslaw
Nicoise Salad (France)
Tabouli (Middle East)
Caprese Salad (Italy)
🌮 MORE GLOBAL SPECIALTIES
Paella Valenciana (Spain variant)
Gnocchi (Italy)
Dim Sum (China)
Tapas (Spain)
Mezze (Middle East)
Sushi Burrito (fusion)
Bao Buns (China)
"""

def generate_massive_dataset():
    lines = [L.strip() for L in RAW_DATA.split("\n") if L.strip()]
    
    current_category = "General"
    keyword = ""
    
    rows = []
    # Start IDs at 201 so we don't conflict with any early 1-100 placeholder recipes 
    # and keep the dataset distinct.
    current_id = 201 
    
    for line in lines:
        if line.startswith("These include"):
            continue
        
        # Detect category header by looking for an emoji at the start
        if any(char in line for char in ["🐐", "🦐", "🦀", "🐑", "🐖", "🐄", "🐔", "🧀", "🟩", "🥦", "🍲", "🐟", "🥚", "🍚", "🍝", "🍟", "🍰", "🥗", "🌮"]):
            current_category = line
            
            # Extract main keyword for generic ingredients
            if "Mutton" in line or "Goat" in line: keyword = "mutton"
            elif "Prawn" in line or "Shrimp" in line: keyword = "prawn"
            elif "Crab" in line: keyword = "crab"
            elif "Lamb" in line: keyword = "lamb"
            elif "Pork" in line: keyword = "pork"
            elif "Beef" in line: keyword = "beef"
            elif "Chicken" in line: keyword = "chicken"
            elif "Paneer" in line: keyword = "paneer"
            elif "Tofu" in line: keyword = "tofu"
            elif "Vegetable" in line: keyword = "vegetables"
            elif "Fish" in line: keyword = "fish"
            elif "Egg" in line: keyword = "eggs"
            elif "Rice" in line: keyword = "rice"
            elif "Cheese" in line: keyword = "cheese"
            else: keyword = "ingredients"
            continue
            
        dish_name = line
        
        # Clean up dish name from parentheticals for the clean name, but keep region info if possible
        clean_name = dish_name
        region = "Global"
        if "(" in dish_name and ")" in dish_name:
            import re
            m = re.search(r'\((.*?)\)', dish_name)
            if m:
                region = m.group(1)
            clean_name = re.sub(r'\(.*?\)', '', dish_name).strip()

        desc = f"A delicious and authentic {clean_name}, honoring traditional {region} cooking methods."
        # Provide somewhat realistic ingredients based on the keyword
        ingredients = [f"500g {keyword}", "2 tbsp cooking oil", "1 large onion, chopped", "2 cloves garlic, minced", "Salt and pepper to taste", "Fresh herbs for garnish"]
        steps = [
            f"Prepare the {keyword} by cleaning and seasoning well.",
            "Heat oil in a pan over medium heat and sauté the chopped onion and minced garlic until fragrant.",
            f"Add the {keyword} and cook thoroughly.",
            "Season with salt, pepper, and regional spices.",
            "Simmer until fully cooked and flavors have melded together.",
            "Garnish with fresh herbs and serve hot."
        ]
        
        tags = [keyword, region.lower().replace(" ", "-"), "authentic"]
        minutes = 45
        
        rows.append({
            'id': current_id,
            'name': clean_name,
            'description': desc,
            'ingredients': str(ingredients).replace('"', "'"),
            'steps': str(steps).replace('"', "'"),
            'tags': str(tags).replace('"', "'"),
            'minutes': minutes,
        })
        current_id += 1
        
    df_new = pd.DataFrame(rows)
    
    # Load existing CSV if it exists
    if os.path.exists(PROCESSED_DATA_PATH):
        df_old = pd.read_csv(PROCESSED_DATA_PATH)
        df_combined = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_combined = df_new
        
    os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
    df_combined.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"Successfully generated {len(df_new)} new recipes in {PROCESSED_DATA_PATH}")
    print(f"Total recipes in dataset: {len(df_combined)}")

if __name__ == "__main__":
    generate_massive_dataset()
