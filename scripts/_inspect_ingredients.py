import pandas as pd, ast

df = pd.read_csv('data/processed/recipes_clean.csv')

print('=== RAW INGREDIENTS SAMPLE (first 6 rows) ===')
for _, row in df.head(6).iterrows():
    print('ID=%s  name=%s' % (row['id'], row['name']))
    print('  ingredients: %s' % repr(str(row['ingredients'])[:250]))
    print()

# Count egg recipes
egg_mask = df['ingredients'].astype(str).str.contains('egg', case=False, na=False)
print('Recipes with "egg" in ingredients: %d' % egg_mask.sum())
for _, row in df[egg_mask].iterrows():
    print('  [%d] %s' % (row['id'], row['name']))

print()

# Count crab recipes
crab_mask = df['ingredients'].astype(str).str.contains('crab', case=False, na=False)
print('Recipes with "crab" in ingredients: %d' % crab_mask.sum())
for _, row in df[crab_mask].iterrows():
    print('  [%d] %s' % (row['id'], row['name']))

print()
print('=== WHAT DOES THE TFIDF ENGINE SEE? ===')
import sys, os
sys.path.insert(0, '.')
from modules.preprocessor import preprocess_dataframe
df2 = preprocess_dataframe(df)
print('ingredient_text for first 3 rows:')
for _, row in df2.head(3).iterrows():
    print('  [%d] %s -> %s' % (row['id'], row['name'], repr(row['ingredient_text'])[:200]))

egg_in_text = df2[df2['ingredient_text'].str.contains('egg', case=False, na=False)]
print()
print('Recipes with "egg" in ingredient_text: %d' % len(egg_in_text))
