/**
 * ChefLogic — main.js  (Phase 8 revision)
 * Features:
 *  - Fuse.js fuzzy autocomplete on ingredient & dish-name inputs
 *  - Quick-add chips: always append comma, allow re-add after backspace
 *  - Search tab switching
 *  - Floating food emoji on click & keypress
 *  - Form loading state
 */

'use strict';

// ── Master Ingredient List ────────────────────────────────────────────────────
const ALL_INGREDIENTS = [
  // Meats
  'mutton', 'minced mutton', 'mutton trotters', 'lamb', 'lamb chops', 'lamb shank',
  'minced lamb', 'chicken', 'chicken breast', 'chicken thigh', 'shredded chicken',
  'chicken wings', 'ground chicken', 'beef', 'ground beef', 'beef ribs', 'beef shank',
  'pork', 'pork belly', 'pork ribs', 'pork shoulder', 'pork loin', 'minced pork',
  'veal', 'bacon', 'ham', 'salami', 'chorizo', 'sausage', 'duck', 'goat',
  'rabbit', 'venison', 'turkey', 'black pudding',
  // Seafood
  'prawn', 'shrimp', 'salmon', 'tuna', 'cod', 'tilapia', 'fish', 'white fish',
  'crab', 'lobster', 'clam', 'mussel', 'squid', 'octopus', 'scallop', 'anchovy',
  'sardine', 'mackerel', 'haddock', 'snapper',
  // Dairy & Eggs
  'egg', 'egg yolk', 'egg white', 'butter', 'milk', 'cream', 'sour cream',
  'heavy cream', 'coconut cream', 'cheddar cheese', 'mozzarella', 'parmesan',
  'feta cheese', 'gruyere', 'ricotta', 'mascarpone', 'gouda', 'brie',
  'cream cheese', 'paneer', 'yogurt', 'ghee', 'condensed milk', 'milk powder',
  // Vegetables
  'onion', 'red onion', 'spring onion', 'shallot', 'garlic', 'ginger',
  'tomato', 'cherry tomato', 'sun dried tomato', 'potato', 'sweet potato',
  'carrot', 'celery', 'broccoli', 'cauliflower', 'spinach', 'kale', 'cabbage',
  'red cabbage', 'lettuce', 'romaine lettuce', 'mixed greens', 'arugula',
  'zucchini', 'eggplant', 'aubergine', 'mushroom', 'shiitake mushroom',
  'porcini mushroom', 'button mushroom', 'capsicum', 'bell pepper', 'red pepper',
  'green pepper', 'yellow pepper', 'pea', 'green bean', 'corn', 'sweet corn',
  'beet', 'beetroot', 'parsnip', 'turnip', 'leek', 'fennel', 'asparagus',
  'artichoke', 'cucumber', 'jalapeño', 'green chili', 'red chili', 'scotch bonnet',
  'bamboo shoot', 'bean sprout', 'bok choy', 'pak choi', 'edamame',
  // Fruits
  'lemon', 'lime', 'orange', 'avocado', 'mango', 'banana', 'apple',
  'apricot', 'fig', 'raisin', 'date', 'pomegranate', 'pineapple', 'coconut',
  'dried cranberry', 'grape', 'olive', 'preserved lemon', 'tamarind',
  // Grains & Pasta
  'basmati rice', 'jasmine rice', 'arborio rice', 'cooked rice', 'sushi rice',
  'brown rice', 'short grain rice', 'long grain rice', 'quinoa', 'oat',
  'spaghetti', 'fettuccine', 'penne', 'rigatoni', 'pasta', 'macaroni',
  'lasagne sheets', 'noodle', 'rice noodle', 'egg noodle', 'ramen noodle',
  'glass noodle', 'bread flour', 'plain flour', 'wheat flour', 'corn flour',
  'chickpea flour', 'almond flour', 'breadcrumb', 'panko breadcrumb',
  'sourdough bread', 'baguette', 'pita', 'naan', 'tortilla', 'taco shell',
  'pizza dough', 'phyllo pastry', 'puff pastry', 'shortcrust pastry',
  'barley', 'lentil', 'red lentil', 'yellow lentil', 'black lentil',
  'wheat', 'couscous', 'bulgur', 'hominy corn', 'polenta', 'cornmeal',
  // Legumes
  'chickpea', 'black bean', 'kidney bean', 'cannellini bean', 'white bean',
  'split pea', 'soybean', 'tofu', 'tempeh', 'miso paste',
  // Nuts & Seeds
  'almond', 'cashew', 'walnut', 'pecan', 'pistachio', 'pine nut', 'peanut',
  'sesame seed', 'sesame oil', 'tahini', 'peanut butter', 'almond butter',
  'sunflower seed', 'pumpkin seed', 'flaxseed',
  // Spices & Herbs
  'cumin', 'coriander', 'turmeric', 'paprika', 'smoked paprika', 'chili powder',
  'garam masala', 'chole masala', 'biryani masala', 'curry powder', 'berbere spice',
  'kashmiri chili', 'cinnamon', 'cardamom', 'clove', 'bay leaf', 'star anise',
  'fennel seed', 'fenugreek', 'mustard seed', 'ajwain', 'black pepper',
  'white pepper', 'sichuan pepper', 'caraway seed', 'nutmeg', 'allspice',
  'saffron', 'vanilla', 'rose water', 'sumac', "za'atar", 'ras el hanout',
  'gochujang', 'doubanjiang', 'miso', 'five spice',
  'basil', 'oregano', 'thyme', 'rosemary', 'parsley', 'cilantro', 'coriander leaf',
  'mint', 'dill', 'sage', 'tarragon', 'lemongrass', 'kaffir lime leaf',
  'curry leaf', 'galangal', 'kasuri methi',
  // Sauces & Condiments
  'soy sauce', 'fish sauce', 'oyster sauce', 'hoisin sauce', 'kecap manis',
  'worcestershire sauce', 'tabasco', 'hot sauce', 'bbq sauce', 'sriracha',
  'tomato sauce', 'tomato paste', 'enchilada sauce', 'teriyaki sauce',
  'ketchup', 'mustard', 'mayonnaise', 'dijon mustard', 'mirin', 'rice vinegar',
  'balsamic vinegar', 'sherry vinegar', 'apple cider vinegar', 'red wine vinegar',
  // Oils & Fats
  'olive oil', 'coconut oil', 'vegetable oil', 'sesame oil', 'sunflower oil',
  'lard', 'vegetable shortening',
  // Liquids
  'coconut milk', 'water', 'chicken broth', 'beef broth', 'vegetable broth',
  'chicken stock', 'beef stock', 'fish stock', 'white wine', 'red wine',
  'dashi', 'tomato juice', 'orange juice', 'apple juice',
  'rum', 'espresso', 'beer', 'sake',
  // Baking
  'sugar', 'brown sugar', 'powdered sugar', 'coconut sugar', 'honey',
  'maple syrup', 'molasses', 'baking powder', 'baking soda', 'yeast',
  'sourdough starter', 'cocoa powder', 'dark chocolate', 'chocolate chips',
  'ladyfinger', 'gelatin', 'corn starch', 'cornstarch',
  // Other
  'salt', 'pepper', 'ice', 'bouquet garni', 'nori', 'seaweed',
  'rice wine', 'tapioca', 'jackfruit', 'kimchi',
  'jameed', 'grape leaf', 'corn tortilla',
];

// ── Fuse.js Fuzzy Search State ────────────────────────────────────────────────
let fuseIngredients = null;  // Fuse instance for local ALL_INGREDIENTS
let fuseRecipeNames = null;  // Fuse instance for recipe names from API

// ── DOM Ready ─────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  fuseIngredients = new Fuse(ALL_INGREDIENTS, {
    threshold: 0.35,
    distance: 120,
    minMatchCharLength: 2,
  });

  fetch('/api/search-data')
    .then(r => r.json())
    .then(data => {
      if (data.names && data.names.length) {
        fuseRecipeNames = new Fuse(data.names, {
          threshold: 0.4,
          distance: 100,
          minMatchCharLength: 2,
        });
      }
      const dishInput = document.getElementById('dish_name');
      const dishDrop  = document.getElementById('dish-fuzzy-dropdown');
      if (dishInput && dishDrop && fuseRecipeNames) {
        attachFuzzySearch(dishInput, dishDrop, fuseRecipeNames, false);
      }
    })
    .catch(() => {});

  const ingInput = document.getElementById('ingredients');
  const ingDrop  = document.getElementById('autocomplete-dropdown');
  if (ingInput && ingDrop) {
    attachFuzzySearch(ingInput, ingDrop, null, true);
  }

  initChips();
  initDishChips();
  initFormLoadingState();
  initInputEnhancements();
  initSearchTabs();
  initMoodCards();
  initEmojiEffect();
  injectDynamicStyles();
  initSettingsMenu();
  initNavFavCount();
  initTabFromSession();
});

// ── Settings Icon Menu ────────────────────────────────────────────────────────
function initSettingsMenu() {
  const btn  = document.getElementById('settings-btn');
  const menu = document.getElementById('settings-menu');
  if (!btn || !menu) return;

  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    const isOpen = menu.classList.toggle('open');
    btn.classList.toggle('open', isOpen);
    btn.setAttribute('aria-expanded', isOpen);
  });

  // Close when clicking anywhere outside
  document.addEventListener('click', () => {
    menu.classList.remove('open');
    btn.classList.remove('open');
    btn.setAttribute('aria-expanded', 'false');
  });

  // Prevent closing when clicking inside the menu
  menu.addEventListener('click', e => e.stopPropagation());
}

// ── Navbar Fav Count Badge ────────────────────────────────────────────────────
function initNavFavCount() {
  const badge = document.getElementById('nav-fav-count');
  const link  = document.getElementById('nav-fav-link');
  if (!badge || !link) return;

  try {
    const favs = JSON.parse(localStorage.getItem('cheflogic_favs') || '[]');
    if (favs.length > 0) {
      badge.textContent = favs.length;
      link.classList.add('has-favs');
    }
  } catch (e) { /* ignore */ }
}

// ── Restore Tab from sessionStorage (e.g. "Mood Search" in settings menu) ────
function initTabFromSession() {
  const tab = sessionStorage.getItem('openTab');
  if (!tab) return;
  sessionStorage.removeItem('openTab');
  const tabBtn = document.getElementById(`tab-${tab}`);
  if (tabBtn) tabBtn.click();
}


// ── Universal Fuzzy Search Wiring ─────────────────────────────────────────────
/**
 * Attaches a Fuse.js fuzzy autocomplete dropdown to an input.
 * @param {HTMLInputElement} inputEl  - the text input
 * @param {HTMLElement}      dropEl   - the dropdown container
 * @param {Fuse|null}        fuseInst - Fuse instance (null = use local ingredient list)
 * @param {boolean}          isIngredient - if true, replaces only the last comma-segment
 */
function attachFuzzySearch(inputEl, dropEl, fuseInst, isIngredient) {
  inputEl.addEventListener('input', () => {
    const full = inputEl.value;
    const query = isIngredient
      ? full.split(',').pop().trim().toLowerCase()
      : full.trim().toLowerCase();

    dropEl.innerHTML = '';
    dropEl.style.display = 'none';

    if (query.length < 1) return;

    // Choose fuse instance
    const fuse = fuseInst || fuseIngredients;
    if (!fuse) return;

    const results = fuse.search(query).slice(0, 8);
    if (!results.length) return;

    results.forEach((r, i) => {
      const item = document.createElement('div');
      item.className = 'ac-item' + (i === 0 ? ' ac-active' : '');
      item.setAttribute('role', 'option');
      item.textContent = r.item;

      item.addEventListener('mousedown', (e) => {
        e.preventDefault();
        if (isIngredient) {
          // Replace only the last typed segment
          const parts = full.split(',');
          parts[parts.length - 1] = ' ' + r.item;
          inputEl.value = parts.join(',') + ', ';
        } else {
          inputEl.value = r.item;
        }
        dropEl.innerHTML = '';
        dropEl.style.display = 'none';
        inputEl.focus();
        const len = inputEl.value.length;
        inputEl.setSelectionRange(len, len);
      });

      dropEl.appendChild(item);
    });

    dropEl.style.display = 'block';
  });

  // Keyboard navigation
  inputEl.addEventListener('keydown', (e) => {
    const items = dropEl.querySelectorAll('.ac-item');
    if (!items.length) return;
    const active = dropEl.querySelector('.ac-active');
    const idx = [...items].indexOf(active);

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      items[idx < 0 ? 0 : Math.min(idx + 1, items.length - 1)]?.classList.add('ac-active');
      if (idx >= 0) items[idx].classList.remove('ac-active');
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (idx > 0) {
        items[idx].classList.remove('ac-active');
        items[idx - 1].classList.add('ac-active');
      }
    } else if (e.key === 'Enter' && active) {
      e.preventDefault();
      active.dispatchEvent(new Event('mousedown'));
    } else if (e.key === 'Escape') {
      dropEl.innerHTML = '';
      dropEl.style.display = 'none';
    }
  });

  // Close on outside click
  document.addEventListener('click', (e) => {
    if (!inputEl.contains(e.target) && !dropEl.contains(e.target)) {
      dropEl.innerHTML = '';
      dropEl.style.display = 'none';
    }
  });
}

// ── Quick-Add Ingredient Chips ────────────────────────────────────────────────
function initChips() {
  const chips = document.querySelectorAll('.chip[data-ingredient]');
  const input = document.getElementById('ingredients');
  if (!chips.length || !input) return;

  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      const ingredient = chip.dataset.ingredient;
      const current = input.value.trim();

      // Already in the list?
      const existing = current.split(',').map(s => s.trim().toLowerCase()).filter(Boolean);
      if (existing.includes(ingredient.toLowerCase())) {
        shakeInput(input);
        return;
      }

      // Append with a trailing comma + space so user can immediately type the next one
      input.value = current ? `${current}, ${ingredient}, ` : `${ingredient}, `;
      chip.classList.add('active');
      // Scroll input to end
      input.focus();
      input.setSelectionRange(input.value.length, input.value.length);

      // Watch for the ingredient to be removed (backspaced out) → reset chip
      const resetOnRemove = () => {
        const parts = input.value.split(',').map(s => s.trim().toLowerCase()).filter(Boolean);
        if (!parts.includes(ingredient.toLowerCase())) {
          chip.classList.remove('active');
          input.removeEventListener('input', resetOnRemove);
        }
      };
      input.addEventListener('input', resetOnRemove);
    });
  });
}

function shakeInput(el) {
  el.style.animation = 'none';
  el.offsetHeight; // force reflow
  el.style.animation = 'shake 0.35s ease';
  setTimeout(() => { el.style.animation = ''; }, 400);
}

// ── Dish Quick-Pick Chips ─────────────────────────────────────────────────────
function initDishChips() {
  const chips = document.querySelectorAll('.dish-chip[data-dish]');
  const input = document.getElementById('dish_name');
  if (!chips.length || !input) return;

  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      input.value = chip.dataset.dish;
      chips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      input.focus();
    });
  });
}

// ── Form Loading State ────────────────────────────────────────────────────────
function initFormLoadingState() {
  [['search-form', 'submit-btn', 'ingredients'],
   ['dish-search-form', 'dish-submit-btn', 'dish_name']].forEach(([formId, btnId, inputId]) => {
    const form = document.getElementById(formId);
    const btn  = document.getElementById(btnId);
    if (!form || !btn) return;

    form.addEventListener('submit', (e) => {
      const inp = document.getElementById(inputId);
      if (!inp || !inp.value.trim()) {
        e.preventDefault();
        inp && inp.focus();
        return;
      }
      btn.classList.add('loading');
      btn.disabled = true;
      setTimeout(() => { btn.classList.remove('loading'); btn.disabled = false; }, 10000);
    });
  });
}

// ── Input UX ──────────────────────────────────────────────────────────────────
function initInputEnhancements() {
  const input = document.getElementById('ingredients');
  const hint  = document.getElementById('ingredients-hint');
  if (!input || !hint) return;

  input.addEventListener('input', () => {
    const count = input.value.split(',').filter(s => s.trim()).length;
    const remaining = 20 - count;
    if (count > 0) {
      hint.textContent = `${count} ingredient${count !== 1 ? 's' : ''} entered — ${remaining > 0 ? `${remaining} more allowed` : 'maximum reached'}`;
    } else {
      hint.textContent = 'Separate multiple ingredients with commas. Max 20 ingredients.';
    }
  });
}

// ── Search Tabs ───────────────────────────────────────────────────────────────
function initSearchTabs() {
  const tabs = document.querySelectorAll('.search-tab');
  if (!tabs.length) return;

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => { t.classList.remove('active'); t.setAttribute('aria-selected', 'false'); });
      document.querySelectorAll('.search-panel').forEach(p => p.classList.add('hidden'));

      tab.classList.add('active');
      tab.setAttribute('aria-selected', 'true');
      const panel = document.getElementById(tab.getAttribute('aria-controls'));
      if (panel) {
        panel.classList.remove('hidden');
        const firstInput = panel.querySelector('input, button, label');
        if (firstInput && firstInput.tagName !== 'LABEL') firstInput.focus();
      }
    });
  });
}

// ── Mood Cards ────────────────────────────────────────────────────────────────
function initMoodCards() {
  const cards = document.querySelectorAll('.mood-card');
  if (!cards.length) return;

  cards.forEach(card => {
    card.addEventListener('click', () => {
      // Visual selection
      cards.forEach(c => c.classList.remove('selected'));
      card.classList.add('selected');

      // Short delay then auto-submit if a radio is now checked
      const radio = card.querySelector('input[type="radio"]');
      if (radio) {
        radio.checked = true;
        // Show a quick ripple animation on the card
        card.style.transition = 'transform 0.15s ease, box-shadow 0.15s ease';
      }
    });
  });
}


// ── Floating Food Emoji Effect ────────────────────────────────────────────────
const FOOD_EMOJIS = ['🍕', '🍔', '🌮', '🍜', '🍛', '🥘', '🍣', '🍤', '🥗', '🍝',
                     '🥩', '🍗', '🦐', '🦀', '🧀', '🥚', '🌯', '🥙', '🍱', '🍲'];

function spawnEmoji(x, y) {
  const container = document.getElementById('emoji-float-container');
  if (!container) return;
  const el = document.createElement('span');
  el.className = 'emoji-float';
  el.textContent = FOOD_EMOJIS[Math.floor(Math.random() * FOOD_EMOJIS.length)];
  el.style.left = `${x - 12}px`;
  el.style.top  = `${y - 12}px`;
  el.style.setProperty('--dx', `${(Math.random() - 0.5) * 60}px`);
  container.appendChild(el);
  setTimeout(() => el.remove(), 1400);
}

function initEmojiEffect() {
  let lastKey = 0;
  document.addEventListener('click', (e) => spawnEmoji(e.clientX, e.clientY));

  document.addEventListener('keydown', () => {
    const now = Date.now();
    if (now - lastKey < 200) return;
    lastKey = now;
    const active = document.activeElement;
    if (active && (active.tagName === 'INPUT' || active.tagName === 'TEXTAREA')) {
      const rect = active.getBoundingClientRect();
      spawnEmoji(rect.left + Math.random() * rect.width, rect.top + Math.random() * 20);
    }
  });
}

// ── Dynamic Styles (shake keyframe) ──────────────────────────────────────────
function injectDynamicStyles() {
  const style = document.createElement('style');
  style.textContent = `
    @keyframes shake {
      0%,100% { transform: translateX(0); }
      20%      { transform: translateX(-6px); }
      40%      { transform: translateX(6px); }
      60%      { transform: translateX(-4px); }
      80%      { transform: translateX(4px); }
    }
    .form-group { position: relative; }
  `;
  document.head.appendChild(style);
}
