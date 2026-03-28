"""
Deep diagnosis: test the real recommender pipeline end-to-end
to understand why egg/crab searches miss recipes.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.data_loader import load_recipes
from modules.preprocessor import preprocess_dataframe

df_raw = load_recipes()   # Uses _safe_parse_list - real pipeline

print('=== SAMPLE INGREDIENTS AFTER _safe_parse_list ===')
for _, row in df_raw.head(4).iterrows():
    print('ID=%s  %s' % (row['id'], row['name']))
    ings = row['ingredients']
    print('  type=%s  len=%s' % (type(ings).__name__, len(ings) if isinstance(ings, list) else 'N/A'))
    if isinstance(ings, list):
        for i in ings[:3]:
            print('    - %s' % i)
    print()

df2 = preprocess_dataframe(df_raw)

print('=== INGREDIENT_TEXT AFTER PREPROCESS (first 4) ===')
for _, row in df2.head(4).iterrows():
    print('ID=%s  %s' % (row['id'], row['name']))
    print('  ingredient_text: %s' % repr(row['ingredient_text'])[:300])
    print()

# Check egg
egg_rows = df2[df2['ingredient_text'].str.contains('egg', case=False, na=False)]
print('Recipes with "egg" in ingredient_text: %d' % len(egg_rows))
for _, r in egg_rows.iterrows():
    print('  [%d] %s' % (r['id'], r['name']))

print()
# Check crab
crab_rows = df2[df2['ingredient_text'].str.contains('crab', case=False, na=False)]
print('Recipes with "crab" in ingredient_text: %d' % len(crab_rows))
for _, r in crab_rows.iterrows():
    print('  [%d] %s' % (r['id'], r['name']))

print()
# Now test the full recommender scoring
from modules.recommender import Recommender
rec = Recommender()
rec.load()

egg_results = rec.recommend('egg', top_n=300)
print('Recommender results for "egg": %d' % len(egg_results))
for r in egg_results:
    print('  [%d] %s  score=%.1f' % (r['id'], r['name'], r['similarity_score']))

print()
crab_results = rec.recommend('crab')
print('Recommender results for "crab": %d' % len(crab_results))
for r in crab_results:
    print('  [%d] %s  score=%.1f' % (r['id'], r['name'], r['similarity_score']))
