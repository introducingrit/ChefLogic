"""
Generate an expanded synthetic dataset with EXTREMELY HIGH DETAIL.
Includes exact measurements (e.g. '500g mutton', '2 tbsp olive oil')
and step-by-step instructions with timings.
Run: python scripts/generate_sample_data.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from config import PROCESSED_DATA_PATH

# Each recipe: (id, name, description, ingredients_list, steps_list, tags_list, minutes)
RECIPES = [
    # ── MUTTON / LAMB ──────────────────────────────────────────────────
    (1,  'Authentic Mutton Biryani',
         'A royal, incredibly aromatic slow-cooked biryani loaded with tender mutton chunks, fragrant spices, and fluffy basmati rice.',
         "['500g mutton on bone, cut into pieces', '2 cups premium basmati rice, soaked for 30 mins', '3 large onions, thinly sliced', '1 cup plain yogurt', '4 tbsp ghee', '1 pinch saffron threads soaked in milk', '2 tbsp biryani masala', '1 tbsp ginger garlic paste', 'Whole spices (cardamom, clove, cinnamon, bay leaf)']",
         "['Marinate the mutton pieces in yogurt, ginger garlic paste, and half the spices for at least 2 hours.', 'In a heavy-bottom pan, heat ghee and fry the sliced onions until golden brown and crispy (about 15 minutes). Remove half for garnish.', 'Add the marinated mutton to the pan and cook on medium-high heat for 10 minutes until browned.', 'Add 1 cup of water, cover, and slow cook the mutton for 45-50 minutes until tender.', 'Meanwhile, boil 4 cups of water with whole spices and salt. Add soaked rice and cook for 8-10 minutes until 70% done. Drain well.', 'Layer the partially cooked rice over the mutton curry. Drizzle with saffron milk, remaining ghee, and fried onions.', 'Cover tightly with a lid (dum) and cook on very low heat for 20-25 minutes.', 'Let it rest for 10 minutes before serving hot with raita.']",
         "['indian', 'mutton', 'rice', 'biryani']", 120),
    (2,  'Mutton Rogan Josh',
         'A signature Kashmiri delicacy featuring rich, deep-red mutton curry infused with warm spices and yogurt.',
         "['500g mutton shoulder, cubed', '1 tbsp Kashmiri chili powder', '1 cup whisked yogurt', '2 large onions, pureed', '1 tbsp garlic paste', '1 tbsp ginger paste', '4 green cardamoms', '4 cloves', '2 bay leaves', '3 tbsp mustard oil or ghee']",
         "['Heat mustard oil in a heavy pot until smoking, then lower the heat. Add whole spices and fry for 30 seconds.', 'Add the onion puree and fry for 10 minutes until it turns light brown.', 'Add ginger and garlic pastes, and stir for another 2 minutes.', 'Add the mutton cubes and roast them on high heat for 10-12 minutes until deeply browned on all sides.', 'Lower the heat, add Kashmiri chili powder and whisked yogurt continuously to prevent curdling.', 'Add 2 cups of warm water, season with salt, cover, and simmer gently for 60-75 minutes until the mutton is spoon-tender.', 'Garnish with fresh coriander and serve hot with naan.']",
         "['indian', 'kashmiri', 'mutton', 'curry']", 90),
    (3,  'Classic Mutton Curry',
         'A hearty, homestyle thick mutton gravy made with a robust base of caramelized onions and tomatoes.',
         "['500g mutton, chopped', '2 large onions, finely chopped', '2 large tomatoes, pureed', '1 tbsp garlic paste', '1 tbsp ginger paste', '1 tsp cumin seeds', '2 tbsp coriander powder', '1 tsp turmeric powder', '1 tsp red chili powder', '3 tbsp vegetable oil']",
         "['Heat oil in a pressure cooker or heavy pot. Add cumin seeds and let them splutter for 30 seconds.', 'Add finely chopped onions and sauté for 10-12 minutes until deeply golden.', 'Stir in ginger and garlic pastes, cooking for 2 minutes until the raw smell disappears.', 'Add the tomato puree, turmeric, red chili, and coriander powder. Cook for 8-10 minutes until the oil separates from the masala.', 'Add the mutton pieces and roast in the masala for 10 minutes, stirring frequently.', 'Pour in 2 cups of water, season with salt, and bring to a boil.', 'Cover and pressure cook for 4 whistles (or simmer covered in a pot for 60 minutes).', 'Let the pressure release naturally. Stir and serve hot with steamed rice.']",
         "['indian', 'mutton', 'curry']", 75),
    (4,  'Lamb Chops with Rosemary',
         'Elegant and juicy pan-seared lamb chops infused with fresh rosemary, garlic, and sea salt.',
         "['8 lamb chops, trimmed', '2 sprigs fresh rosemary, finely chopped', '3 cloves garlic, minced', '3 tbsp extra virgin olive oil', '1 tsp lemon zest', '1 tsp black pepper, freshly cracked', '1 tsp sea salt']",
         "['In a small bowl, mix the olive oil, minced garlic, chopped rosemary, lemon zest, salt, and black pepper.', 'Rub the marinade generously over both sides of the lamb chops.', 'Let the chops marinate at room temperature for at least 30 minutes.', 'Preheat a heavy cast-iron skillet over medium-high heat until very hot.', 'Place the lamb chops in the dry skillet (the oil in the marinade is enough).', 'Sear for 3-4 minutes on the first side until a dark brown crust forms.', 'Flip and cook for another 3 minutes for medium-rare, or 4-5 minutes for medium.', 'Remove from heat, tent with foil, and let rest for 5 minutes before serving.']",
         "['mediterranean', 'lamb', 'grill', 'gluten-free']", 45),
    (5,  'Irish Lamb Stew',
         'A traditional, comforting one-pot stew brimming with tender lamb shoulder, pearl barley, and root vegetables.',
         "['700g boneless lamb shoulder, cut into 2-inch chunks', '4 large potatoes, peeled and quartered', '4 carrots, cut into thick rounds', '2 large onions, thickly sliced', '1 litre lamb or beef stock', '1 tbsp fresh thyme leaves', '2 bay leaves', '1/4 cup pearl barley']",
         "['Season the lamb chunks generously with salt and pepper.', 'In a large heavy-bottomed pot, brown the lamb in batches over medium-high heat (about 5 mins per batch). Remove and set aside.', 'In the same pot, add onions and carrots, sautéing for 5 minutes until slightly softened.', 'Return the lamb to the pot along with the lamb stock, thyme, bay leaves, and pearl barley.', 'Bring to a boil, then reduce heat to low, cover, and simmer for 1 hour.', 'Add the quartered potatoes to the pot. Cover and continue to simmer for another 45-60 minutes until the meat and potatoes are very tender.', 'Taste and adjust seasoning. Discard the bay leaves before serving hot in bowls.']",
         "['irish', 'european', 'lamb', 'stew']", 130),

    # ── CHICKEN ──────────────────────────────────────────────────────────────
    (6,  'Restaurant Style Butter Chicken',
         'A globally loved Indian classic featuring charred chicken pieces in a silky, rich, buttery tomato sauce.',
         "['500g boneless chicken thighs, cut into bite-sized pieces', '3 tbsp butter', '4 large tomatoes, pureed', '1/2 cup heavy cream', '1 tbsp garam masala', '1 tbsp ginger garlic paste', '1 tbsp kasuri methi (dried fenugreek leaves)', '1/2 cup plain yogurt', '1 tsp Kashmiri chili powder']",
         "['Marinate the chicken pieces in yogurt, half the ginger garlic paste, and Kashmiri chili powder for 1 hour.', 'Preheat oven to 200°C (400°F). Thread chicken onto skewers and bake for 15-20 minutes until charred at the edges.', 'In a large pan, melt 2 tbsp butter over medium heat. Add remaining ginger garlic paste and fry for 1 minute.', 'Add the tomato puree and cook for 15 minutes, stirring occasionally, until the sauce thickens and oil begins to separate.', 'Stir in garam masala and salt. Add the baked chicken pieces and simmer for 5-7 minutes.', 'Lower the heat, stir in the heavy cream and crushed kasuri methi.', 'Simmer for 2 final minutes. Top with remaining 1 tbsp butter and a swirl of cream. Serve with naan.']",
         "['indian', 'chicken', 'curry']", 85),
    (7, 'Classic Chicken Tikka Masala',
         'Tender, grilled chicken chunks enveloped in a highly spiced, vibrant, and creamy tomato gravy.',
         "['600g chicken breast, cubed', '400g canned crushed tomatoes', '1/2 cup heavy cream', '2 tbsp garam masala', '4 cloves garlic, minced', '1 tbsp fresh ginger, grated', '1 cup plain yogurt', '1 tsp ground cumin', '1 tsp paprika', '2 tbsp vegetable oil']",
         "['Mix yogurt, 1 tbsp garam masala, cumin, half the garlic, and half the ginger. Coat the chicken and marinate for 2 hours.', 'Heat 1 tbsp oil in a large skillet over high heat. Sear the chicken pieces in batches for 3-4 minutes per side until browned. Set aside.', 'In the same skillet, heat remaining oil. Add remaining garlic and ginger, cooking for 1 minute until fragrant.', 'Stir in the crushed tomatoes, paprika, and remaining 1 tbsp garam masala. Bring to a simmer and cook for 15 minutes.', 'Return the browned chicken to the skillet. Reduce heat to low and simmer for 10 minutes until chicken is cooked through.', 'Stir in the heavy cream and warm through for 2 minutes (do not boil).', 'Garnish with fresh cilantro and serve with basmati rice.']",
         "['indian', 'british', 'chicken', 'curry']", 135),
    (8, 'Chicken Stir Fry with Vegetables',
         'A fast, vibrant, and healthy asian stir-fry with broccoli, bell peppers, and chicken in a savory soy-sesame glaze.',
         "['400g chicken breast, thinly sliced against the grain', '2 cups broccoli florets', '3 tbsp soy sauce', '3 cloves garlic, finely minced', '1 tbsp ginger, grated', '1 tbsp sesame oil', '1 red bell pepper, sliced into strips', '1 tbsp cornstarch', '2 tbsp vegetable oil']",
         "['In a small bowl, whisk together soy sauce, sesame oil, and cornstarch. Toss the sliced chicken in half of this marinade and let rest for 15 minutes.', 'Heat 1 tbsp vegetable oil in a wok or large skillet over high heat until smoking.', 'Add the chicken in a single layer. Let it sear undisturbed for 2 minutes, then stir-fry for 3 more minutes until browned and cooked through. Remove to a plate.', 'Wipe the wok clean if necessary, add remaining 1 tbsp oil. Add garlic and ginger, tossing for 15 seconds.', 'Add the broccoli and bell pepper. Stir-fry for 3 minutes until crisp-tender. (Add a splash of water if the pan gets too dry).', 'Return the chicken to the wok. Pour in the remaining soy sauce mixture.', 'Toss everything continuously for 1-2 minutes until the sauce bubbles and thickens, coating the chicken and vegetables evenly.', 'Serve immediately over hot jasmine rice.']",
         "['asian', 'chinese', 'chicken']", 30),

    # ── BEEF ─────────────────────────────────────────────────────────────────
    (9, 'Classic Beef Stew',
         'The ultimate comfort food: chunks of tender beef chuck simmered very slowly with potatoes and carrots.',
         "['800g beef chuck roast, cut into 1.5-inch cubes', '3 large potatoes, peeled and cubed', '4 carrots, peeled and cut into 1-inch pieces', '1 large yellow onion, chopped', '4 cups beef broth', '1 tsp dried thyme', '2 bay leaves', '2 tbsp tomato paste', '3 tbsp all-purpose flour', '2 tbsp olive oil']",
         "['Season the beef cubes with salt and pepper, then toss them in the flour until evenly coated.', 'Heat olive oil in a large Dutch oven over medium-high heat. Brown the beef in batches, ensuring a good crust on all sides (about 3-4 mins per batch). Remove and set aside.', 'Add the chopped onion to the pot, sautéing for 5 minutes until softened.', 'Stir in the tomato paste and cook for 2 minutes until it darkens slightly.', 'Pour in the beef broth, scraping the browned bits from the bottom of the pot. Return the beef along with the thyme and bay leaves.', 'Bring to a boil, reduce the heat to a low simmer, cover, and cook for 1.5 hours.', 'Add the cubed potatoes and carrots. Cover and simmer for another 45 minutes until the vegetables and meat are completely tender.', 'Remove the bay leaves, taste for seasoning, and serve hot with crusty bread.']",
         "['american', 'european', 'beef']", 150),
    (10, 'Beef Burger with Caramelised Onions',
         'A towering, juicy beef patty topped with sharply aged cheddar and deeply sweet, slow-cooked caramelised onions.',
         "['500g 80% lean ground beef', '4 brioche burger buns', '4 crisp lettuce leaves', '2 tomatoes, sliced thick', '2 large white onions, thinly sliced', '4 slices aged cheddar cheese', '2 tbsp ketchup', '1 tbsp yellow mustard', '2 tbsp butter']",
         "['Melt 1 tbsp butter in a skillet over low heat. Add the sliced onions and a pinch of salt. Cook very slowly for 35-40 minutes, stirring occasionally, until they are deep brown and sweet. Set aside.', 'Divide the ground beef into 4 equal portions and gently form them into patties slightly wider than your buns. Make a slight indentation in the center of each. Season generously with salt and pepper.', 'Heat a grill or cast-iron skillet over medium-high heat until very hot.', 'Place the patties on the heat and cook undisturbed for 4 minutes until a crust forms.', 'Flip the burgers, top each with a slice of cheddar cheese, and cook for 3-4 more minutes for medium doneness.', 'Meanwhile, toast the brioche buns with the remaining butter.', 'Assemble the burgers: bottom bun, ketchup/mustard, lettuce, tomato, cheeseburger patty, caramelised onions, top bun. Serve immediately.']",
         "['american', 'beef']", 55),

    # ── SEAFOOD ───────────────────────────────────────────────────────────────
    (11, 'Garlic Herb Grilled Salmon',
         'A beautifully flaky salmon fillet kissed with fire, marinated in bright lemon, garlic, and fresh dill.',
         "['4 salmon fillets (about 170g each)', '1 large lemon, juiced and zested', '4 cloves garlic, minced', '3 tbsp extra virgin olive oil', '1 tbsp fresh dill, chopped', '1 tsp sea salt', '1/2 tsp crushed black pepper']",
         "['In a small bowl, whisk together the olive oil, lemon juice, lemon zest, minced garlic, chopped dill, salt, and pepper.', 'Place the salmon fillets in a shallow dish and pour the marinade over them. Let them marinate at room temperature for 15-20 minutes.', 'Preheat a grill or a grill pan over medium-high heat. Brush the grates lightly with oil.', 'Place the salmon fillets skin-side down on the grill. Cook for 4-5 minutes without moving them, allowing the skin to crisp.', 'Carefully flip the salmon and cook for an additional 3-4 minutes until the flesh is opaque and flakes easily with a fork.', 'Transfer to a serving platter, let rest for 3 minutes, and serve with extra lemon wedges.']",
         "['american', 'european', 'seafood', 'fish', 'gluten-free']", 30),
    (12, 'Spicy Prawn Masala',
         'Juicy pink prawns tossed in a fiery, thick, and highly aromatic coconut and tomato masala base.',
         "['400g large prawns, peeled and deveined', '2 medium onions, finely chopped', '2 large tomatoes, blended to a paste', '1/4 cup freshly grated coconut', '4 cloves garlic, crushed', '1 inch ginger, grated', '1 tsp red chili powder', '1/2 tsp turmeric powder', '1 sprig curry leaves', '2 tbsp coconut oil']",
         "['Grind the grated coconut with 2 tbsp of water into a smooth, thick paste. Set aside.', 'Heat coconut oil in a pan over medium heat. Add the curry leaves and wait for them to crackle (about 10 seconds).', 'Add the finely chopped onions and sauté for 8-10 minutes until they turn golden brown.', 'Stir in the crushed garlic and grated ginger, cooking for 2 minutes until fragrant.', 'Add the tomato paste, red chili powder, and turmeric. Cook for 10-12 minutes until the masala thickens and oil begins to separate at the edges.', 'Stir in the coconut paste and 1/2 cup of warm water. Bring to a gentle simmer.', 'Add the cleaned prawns and season with salt. Cook for exactly 5-6 minutes until the prawns curl and turn opaque and pink. Do not overcook.', 'Garnish with fresh coriander and serve hot with steamed rice or paratha.']",
         "['indian', 'coastal', 'seafood', 'prawn', 'gluten-free']", 35),

    # ── VEGETARIAN / VEGAN ─────────────────────────────────────────────────────
    (13, 'Paneer Butter Masala',
         'A lush, extraordinarily creamy vegetarian curry featuring soft cubes of paneer in a spiced tomato-cashew base.',
         "['400g paneer, cut into thick cubes', '4 large ripe tomatoes, roughly chopped', '1/4 cup cashew nuts', '3 tbsp unsalted butter', '3 tbsp heavy cream', '1 large onion, roughly chopped', '1 tbsp garam masala', '1 tbsp kasuri methi (dried fenugreek)', '1 tbsp ginger paste', '1 tbsp garlic paste']",
         "['In a large pan, heat 1 tbsp of butter. Add the roughly chopped onions, tomatoes, and cashew nuts. Sauté for 10 minutes until tomatoes are mushy.', 'Let the mixture cool slightly, then transfer to a blender and blend into a very smooth, fine puree.', 'In the same pan, heat the remaining 2 tbsp of butter over medium-low heat. Add the ginger and garlic pastes, frying for 1 minute.', 'Pour the blended tomato-cashew puree back into the pan. Bring to a simmer and cook for 10-12 minutes, stirring occasionally, until the sauce thickens.', 'Stir in the garam masala and salt. Add the paneer cubes and simmer gently for 5 minutes so the paneer absorbs the flavors without breaking.', 'Crush the kasuri methi between your palms and sprinkle it into the sauce along with the heavy cream.', 'Stir gently for 1 minute, then turn off the heat. Serve hot with garlic naan.']",
         "['indian', 'vegetarian', 'paneer']", 45),
    (14, 'Authentic Dal Tadka',
         'A staple Indian yellow lentil dish finished with a sizzling, smoky tempering of garlic, cumin, and ghee.',
         "['1 cup yellow lentils (toor dal), washed thoroughly', '1 medium onion, finely chopped', '1 large tomato, chopped', '4 cloves garlic, thinly sliced', '1 tsp cumin seeds', '1/2 tsp turmeric powder', '1 tsp Kashmiri red chili powder', '2 tbsp ghee (clarified butter)', '2 tbsp fresh coriander, chopped']",
         "['Place the washed lentils in a pressure cooker with 3 cups of water, turmeric powder, and a pinch of salt.', 'Pressure cook for 3-4 whistles (or boil in a pot for 40 minutes) until the lentils are completely soft and mushy. Whisk them lightly.', 'For the first tempering: heat 1 tbsp ghee in a pan. Add chopped onions and cook for 5 minutes until translucent.', 'Add the chopped tomatoes and cook for 5-7 minutes until they break down entirely. Pour this mixture into the cooked lentils and bring to a simmer for 5 minutes.', 'For the final Tadka (tempering): heat the remaining 1 tbsp ghee in a small pan over medium heat.', 'Add the cumin seeds and let them splutter. Add the thinly sliced garlic and fry until golden brown and crispy (do not burn).', 'Turn off the heat, immediately add the Kashmiri red chili powder, and pour the sizzling spiced ghee over the simmering dal.', 'Mix well, garnish with fresh coriander, and serve immediately with jeera rice.']",
         "['indian', 'vegetarian', 'vegan', 'lentil', 'gluten-free']", 40),
    (15, 'Mushroom Risotto',
         'A rich, fine-dining quality Italian rice dish, deeply savory with browned mushrooms, white wine, and parmesan.',
         "['1.5 cups arborio rice', '300g cremini or button mushrooms, sliced', '1/2 cup freshly grated parmesan cheese', '1/2 cup dry white wine', '1 small white onion, finely diced', '3 tbsp unsalted butter', '4 cups hot vegetable stock', '2 cloves garlic, minced', '1 tsp fresh thyme']",
         "['Keep the vegetable stock warm in a saucepan over low heat on a separate burner.', 'In a wide, heavy-bottomed pan or Dutch oven, melt 1 tbsp butter over medium-high heat. Add the sliced mushrooms and cook until browned (about 6-8 minutes). Remove half the mushrooms for garnish.', 'Reduce heat to medium, add 1 tbsp butter, and sauté the diced onion for 4 minutes until translucent.', 'Add the minced garlic and thyme, cooking for 1 minute.', 'Add the arborio rice to the pan and toast it, stirring constantly, for 2-3 minutes until the edges of the grains become translucent.', 'Pour in the white wine and stir continuously until the liquid is almost completely absorbed.', 'Begin adding the hot vegetable stock one ladleful (about 1/2 cup) at a time, stirring constantly and allowing each addition to be absorbed before adding the next. This process will take 18-22 minutes.', 'Once the rice is tender but still has a slight bite (al dente), remove the pan from heat.', 'Vigorously stir in the remaining 1 tbsp butter, parmesan cheese, and the cooked mushrooms. The risotto should be creamy and ooze slowly on a plate.', 'Serve immediately, garnished with the reserved browned mushrooms and extra parmesan.']",
         "['italian', 'vegetarian', 'risotto']", 50),

    # ── PASTA / ITALIAN ────────────────────────────────────────────────────────
    (16, 'Authentic Spaghetti Carbonara',
         'A Roman classic made purely with egg yolks, sharp pecorino cheese, lots of black pepper, and crispy guanciale.',
         "['400g spaghetti', '3 large eggs (room temperature)', '150g crispy bacon or pancetta, diced', '1 cup freshly grated parmesan or pecorino romano', '1 tbsp coarse black pepper, freshly ground', 'Salt for pasta water']",
         "['Bring a large pot of heavily salted water to a rolling boil. Add spaghetti and cook according to package instructions until al dente (usually 9-11 minutes).', 'While pasta cooks, heat a large dry skillet over medium heat. Add the diced bacon/pancetta and fry slowly for 8-10 minutes until crispy and the fat has rendered. Turn off the heat but leave the meat and fat in the pan.', 'In a serving bowl, whisk the eggs and the grated parmesan cheese together until it forms a thick paste. Mix in the freshly ground black pepper.', 'Before draining the pasta, reserve 1 cup of the starchy pasta water.', 'Using tongs, quickly transfer the hot, dripping spaghetti directly from the water into the skillet with the bacon and toss to coat in the fat.', 'Immediately transfer the pasta and bacon mixture into the bowl with the egg and cheese mixture. Working very quickly, toss continuously so the residual heat from the pasta cooks the eggs into a silky sauce without scrambling them.', 'Add splashes of the reserved pasta water (1-2 tablespoons at a time) as you toss, until the sauce reaches a creamy consistency.', 'Serve immediately and top with extra pepper and cheese.']",
         "['italian', 'pasta']", 25),

    # ── ASIAN ────────────────────────────────────────────────────────────────
    (17, 'Authentic Pad Thai',
         'Thailand’s most famous street food: sweet, tangy, and savory stir-fried rice noodles with eggs and crushed peanuts.',
         "['200g flat rice noodles', '200g shrimp, peeled and deveined', '2 large eggs, lightly beaten', '1 cup fresh bean sprouts', '1/2 cup roasted peanuts, roughly crushed', '3 tbsp fish sauce', '1 lime, cut into wedges', '3 tbsp tamarind paste', '4 spring onions, cut into 2-inch pieces', '2 tbsp vegetable oil', '1 tbsp palm sugar or brown sugar']",
         "['Soak the rice noodles in warm (not boiling) water for 30-40 minutes until they are pliable but completely firm. Drain and set aside.', 'In a small bowl, whisk together the tamarind paste, fish sauce, and palm sugar until the sugar is dissolved. This is your Pad Thai sauce.', 'Heat a large wok or skillet over high heat until very hot. Add 1 tbsp oil, and stir-fry the shrimp for 2 minutes until pink. Remove and set aside.', 'Wipe the wok if needed, add remaining 1 tbsp oil. Pour in the beaten eggs and quickly scramble them for 30 seconds.', 'Before the eggs fully set, add the drained rice noodles to the wok. Pour the Pad Thai sauce over the noodles.', 'Toss vigorously for 3-4 minutes, lifting the noodles so they cook evenly and absorb the sauce without breaking.', 'Add the cooked shrimp, bean sprouts, spring onions, and half the crushed peanuts to the wok. Toss everything together for 1 final minute until the vegetables are just heated through but still crunchy.', 'Serve immediately, garnished with the remaining peanuts and lime wedges on the side for squeezing.']",
         "['thai', 'asian', 'seafood']", 45),

    # ── BREAKFAST ────────────────────────────────────────────────────────────
    (18, 'Perfect Fluffy Pancakes',
         'A towering stack of incredibly light, thick, and fluffy American diner-style morning pancakes.',
         "['1.5 cups all-purpose flour', '2 large eggs', '1.25 cups milk', '3 tbsp melted butter', '2 tbsp granulated sugar', '3.5 tsp baking powder', '1 tsp vanilla extract', '1/2 tsp salt', 'Maple syrup for serving']",
         "['In a large bowl, sift together the flour, baking powder, salt, and sugar. Make a well in the center.', 'In a separate medium bowl, whisk together the eggs, milk, melted butter, and vanilla extract until smooth.', 'Pour the wet ingredients into the well of the dry ingredients. Use a whisk or fork to gently mix until just combined.', 'Do not overmix; the batter should be slightly lumpy. Let the batter rest for 5-10 minutes. This is crucial for fluffiness.', 'Heat a lightly oiled griddle or non-stick frying pan over medium-high heat. Once hot, lower the heat to medium.', 'Pour or scoop the batter onto the griddle, using approximately 1/4 cup for each pancake.', 'Cook for about 2-3 minutes, until bubbles form on the surface of the pancake and the edges look set and dry.', 'Flip carefully with a wide spatula and cook the other side for 1-2 minutes until golden brown.', 'Serve warm immediately, stacked high, with butter and maple syrup.']",
         "['american', 'breakfast', 'vegetarian']", 25),

    # ── DESSERTS ─────────────────────────────────────────────────────────────
    (19, 'Molten Chocolate Lava Cake',
         'A decadent, rich individual dessert with a perfectly baked dark chocolate exterior and a flowing liquid center.',
         "['115g high-quality dark chocolate (70%), chopped', '115g unsalted butter, plus extra for greasing', '3 large eggs', '1/2 cup granulated sugar', '1/4 cup all-purpose flour', '1 tsp pure vanilla extract', '1 tbsp cocoa powder, for dusting the ramekins']",
         "['Preheat your oven to 220°C (425°F). Generously butter four 6-ounce ramekins, then thoroughly dust the insides with cocoa powder, tapping out the excess.', 'Place the chopped dark chocolate and 115g butter in a heatproof bowl set over a saucepan of barely simmering water (a double boiler). Stir occasionally until completely melted and smooth. Remove from heat and let cool slightly.', 'In a separate large bowl, use an electric mixer or a whisk to beat the eggs and sugar on high speed for about 3 minutes, until pale, thick, and greatly increased in volume.', 'Gently fold the warm melted chocolate mixture and the vanilla extract into the whipped eggs using a silicone spatula.', 'Sift the flour over the mixture and fold it in very gently just until the flour disappears. Do not overmix.', 'Divide the batter evenly among the prepared ramekins. Place the ramekins on a baking sheet.', 'Bake for exactly 11-13 minutes. The edges should be set and baked, but the centers should still look soft and slightly jiggly.', 'Remove from the oven and let rest for exactly 1 minute.', 'Carefully run a thin knife around the edges, place an upside-down serving plate over the ramekin, and invert. Gently lift off the ramekin to reveal the cake.', 'Serve immediately with vanilla ice cream or a dusting of powdered sugar.']",
         "['french', 'american', 'dessert']", 35),
         
    # ── MEXICAN ────────────────────────────────────────────────────────────
    (20, 'Authentic Guacamole',
         'A fresh, bright, and chunky avocado dip spiced with sharp red onion, jalapeño, and loads of fresh lime.',
         "['3 ripe Hass avocados', '1 lime, juiced', '1/2 medium red onion, very finely diced', '1 large Roma tomato, seeds removed and finely diced', '1/4 cup fresh cilantro (coriander), roughly chopped', '1 jalapeño pepper, seeds removed and minced', '1 tsp flaky sea salt', '1 clove garlic, minced to a paste']",
         "['Cut the avocados in half, remove the pits, and scoop the flesh into a large mixing bowl.', 'Immediately pour the fresh lime juice over the avocado. This flavors it and prevents browning.', 'Using a fork or a potato masher, mash the avocado gently. Leave it slightly chunky for the best authentic texture; do not mash to a smooth puree.', 'Add the finely diced red onion, minced garlic, minced jalapeño, and chopped cilantro to the bowl.', 'Sprinkle the sea salt over the top.', 'Gently fold the ingredients together until combined.', 'Add the diced tomatoes last, folding them in very gently so they do not turn the guacamole watery.', 'Taste and adjust seasoning, adding more lime or salt if needed. Serve immediately with tortilla chips.']",
         "['mexican', 'vegan', 'vegetarian', 'gluten-free']", 15)
]

# Generate additional placeholder recipes for IDs 21-100
for i in range(21, 101):
    name = f'Global Dish {i}'
    desc = f'A delightful international recipe number {i}, showcasing diverse flavors and cooking techniques.'
    ingredients = [f'1 unit ingredient {j} for dish {i}' for j in range(1, 4)]
    steps = [f'Perform step {j} for dish {i}.' for j in range(1, 4)]
    tags = ['global', f'dish{i}']
    minutes = 30 + (i % 60)
    RECIPES.append((i, name, desc, str(ingredients), str(steps), str(tags), minutes))

rows = []
for r in RECIPES:
    rid, name, desc, ingredients, steps, tags, minutes = r
    rows.append({
        'id': rid,
        'name': name,
        'description': desc,
        'ingredients': ingredients,

        'steps': steps,
        'tags': str(tags).replace('"', "'"),
        'minutes': minutes,
    })

df = pd.DataFrame(rows)
os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
df.to_csv(PROCESSED_DATA_PATH, index=False)
print(f"Created HIGH DETAIL sample dataset: {len(df)} recipes -> {PROCESSED_DATA_PATH}")
print("Contains precise measurements and elaborate cooking processes.")
