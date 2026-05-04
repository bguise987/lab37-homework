"""Run once to populate the database with sample data for development/review."""
from database import Base, SessionLocal, engine
from models import Company, Recipe, User

Base.metadata.create_all(bind=engine)

db = SessionLocal()

if db.query(Company).count() > 0:
    print("Database already seeded, skipping.")
    db.close()
    exit(0)

# Companies
acme = Company(name="Acme Bakery", address="123 Main St, Springfield")
globex = Company(name="Globex Foods", address="456 Industrial Ave, Shelbyville")
bowl_co = Company(name="The Bowl Co.", address="789 Pacific Ave, Portland")
poke_palace = Company(name="Poke Palace", address="321 Ocean Dr, Honolulu")
mesa_verde = Company(name="Mesa Verde Kitchen", address="555 Canyon Rd, Santa Fe")
harvest_table = Company(name="Harvest Table", address="88 Farm Lane, Burlington")
db.add_all([acme, globex, bowl_co, poke_palace, mesa_verde, harvest_table])
db.flush()

# Users
alice = User(username="alice", password="password1")
alice.company_ids = [acme.id]

bob = User(username="bob", password="password2")
bob.company_ids = [globex.id]

# User belonging to both original companies
carol = User(username="carol", password="password3")
carol.company_ids = [acme.id, globex.id]

diana = User(username="diana", password="password4")
diana.company_ids = [bowl_co.id]

evan = User(username="evan", password="password5")
evan.company_ids = [poke_palace.id]

fiona = User(username="fiona", password="password6")
fiona.company_ids = [mesa_verde.id]

grace = User(username="grace", password="password7")
grace.company_ids = [harvest_table.id]

db.add_all([alice, bob, carol, diana, evan, fiona, grace])
db.flush()

# Recipes for Acme
db.add_all([
    Recipe(
        title="Classic Sourdough",
        ingredients="500g bread flour\n375g water\n10g salt\n100g sourdough starter",
        instructions="Mix flour and water, autolyse 30 min.\nAdd starter and salt, fold every 30 min for 3 hrs.\nShape and cold proof overnight.\nBake at 250°C for 45 min.",
        yield_grams=850,
        company_id=acme.id,
        created_by=alice.id,
        last_edited_by=alice.id,
    ),
    Recipe(
        title="Chocolate Chip Cookies",
        ingredients="225g butter\n200g brown sugar\n100g white sugar\n2 eggs\n375g flour\n5g baking soda\n5g salt\n340g chocolate chips",
        instructions="Cream butter and sugars.\nBeat in eggs.\nMix in dry ingredients.\nFold in chocolate chips.\nBake at 190°C for 10-12 min.",
        yield_grams=600,
        company_id=acme.id,
        created_by=alice.id,
        last_edited_by=alice.id,
    ),
])

# Recipe for Globex
db.add_all([
    Recipe(
        title="Tomato Sauce",
        ingredients="800g crushed tomatoes\n4 cloves garlic\n30ml olive oil\n5g salt\n2g black pepper\n5g dried basil",
        instructions="Sauté garlic in olive oil 2 min.\nAdd tomatoes and seasoning.\nSimmer 20 min, stirring occasionally.",
        yield_grams=750,
        company_id=globex.id,
        created_by=bob.id,
        last_edited_by=bob.id,
    ),
])

# Recipes for The Bowl Co.
db.add_all([
    Recipe(
        title="Burrito Bowl",
        ingredients="300g cooked cilantro-lime rice\n200g black beans, seasoned\n180g grilled chicken thigh, sliced\n100g corn kernels\n80g pico de gallo\n60g shredded romaine\n40g sour cream\n30g shredded cheddar\n20g pickled jalapeños\n15ml lime juice",
        instructions="Season rice with lime juice and chopped cilantro.\nWarm black beans with cumin, garlic powder, and salt.\nGrill chicken thighs at 220°C for 6 min per side, rest 5 min, slice.\nLayer rice as base, then beans, chicken, corn, and romaine.\nTop with pico de gallo, sour cream, cheddar, and jalapeños.",
        yield_grams=985,
        company_id=bowl_co.id,
        created_by=diana.id,
        last_edited_by=diana.id,
    ),
    Recipe(
        title="Korean BBQ Bowl",
        ingredients="280g steamed short-grain rice\n200g bulgogi beef\n60ml soy sauce\n30ml sesame oil\n20g brown sugar\n10g minced garlic\n8g grated ginger\n100g quick-pickled cucumber\n80g shredded carrots\n50g kimchi\n30g gochujang mayo\n5g toasted sesame seeds\n3 green onions, sliced",
        instructions="Combine soy sauce, sesame oil, sugar, garlic, and ginger to make bulgogi marinade.\nSlice beef thinly, marinate at least 30 min.\nCook beef in a hot skillet 2-3 min until caramelized.\nToss cucumber with rice vinegar, salt, and sugar; rest 15 min.\nBuild bowl: rice, beef, cucumber, carrots, kimchi.\nDrizzle with gochujang mayo and top with sesame seeds and green onion.",
        yield_grams=866,
        company_id=bowl_co.id,
        created_by=diana.id,
        last_edited_by=diana.id,
    ),
    Recipe(
        title="Falafel and Hummus Bowl",
        ingredients="6 falafel balls (200g)\n150g hummus\n200g couscous, cooked\n100g cherry tomatoes, halved\n80g cucumber, diced\n60g kalamata olives\n40g crumbled feta\n30g tahini\n15ml lemon juice\n5g fresh parsley, chopped\n2g za'atar",
        instructions="Prepare couscous per packet instructions; fluff with a fork.\nBake or pan-fry falafel until crispy, about 15 min at 200°C.\nWhisk tahini with lemon juice and 30ml water until smooth.\nSpread hummus across one side of the bowl, add couscous alongside.\nArrange falafel, tomatoes, cucumber, and olives.\nDrizzle tahini dressing, sprinkle feta, parsley, and za'atar.",
        yield_grams=880,
        company_id=bowl_co.id,
        created_by=diana.id,
        last_edited_by=diana.id,
    ),
])

# Recipes for Poke Palace
db.add_all([
    Recipe(
        title="Classic Ahi Poke Bowl",
        ingredients="300g sushi-grade ahi tuna, cubed\n250g steamed sushi rice\n40ml soy sauce\n15ml sesame oil\n10g grated fresh ginger\n5g sriracha\n80g edamame, shelled\n60g sliced avocado\n40g shredded red cabbage\n30g pickled ginger\n20g cucumber, thinly sliced\n10g furikake\n5g toasted sesame seeds",
        instructions="Mix soy sauce, sesame oil, ginger, and sriracha in a bowl.\nGently toss cubed tuna in marinade; rest 10 min in the refrigerator.\nSeason warm rice lightly with rice vinegar and a pinch of salt.\nArrange rice in bowl, place marinated tuna on top.\nAdd edamame, avocado, cabbage, cucumber, and pickled ginger around the tuna.\nFinish with furikake and sesame seeds.",
        yield_grams=815,
        company_id=poke_palace.id,
        created_by=evan.id,
        last_edited_by=evan.id,
    ),
    Recipe(
        title="Spicy Salmon Poke Bowl",
        ingredients="300g sushi-grade salmon, cubed\n250g steamed sushi rice\n30ml soy sauce\n20ml spicy mayo\n10ml sesame oil\n80g mango, diced\n60g sliced avocado\n50g cucumber, diced\n40g shredded carrots\n30g crispy wonton strips\n10g green onion, sliced\n5g toasted sesame seeds\n5ml lime juice",
        instructions="Combine soy sauce, sesame oil, and half the spicy mayo; fold in salmon cubes.\nMarinate salmon 10 min in the refrigerator.\nSeason rice with lime juice and a pinch of salt.\nLayer rice, then salmon, mango, avocado, cucumber, and carrots.\nDrizzle remaining spicy mayo on top.\nFinish with crispy wonton strips, green onion, and sesame seeds.",
        yield_grams=840,
        company_id=poke_palace.id,
        created_by=evan.id,
        last_edited_by=evan.id,
    ),
    Recipe(
        title="Tofu Poke Bowl",
        ingredients="300g extra-firm tofu, pressed and cubed\n250g steamed brown rice\n40ml tamari\n20ml sesame oil\n15ml rice vinegar\n10g grated ginger\n80g shelled edamame\n70g shredded purple cabbage\n60g sliced avocado\n50g shredded carrots\n40g cucumber, diced\n20g pickled daikon\n10g furikake\n5g toasted sesame seeds",
        instructions="Press tofu for at least 30 min; cube and pat dry.\nMarinate tofu in tamari, half the sesame oil, rice vinegar, and ginger for 20 min.\nBake tofu at 200°C for 25 min, flipping halfway, until golden.\nSeason rice with remaining sesame oil and a pinch of salt.\nBuild bowl: rice, baked tofu, edamame, cabbage, avocado, carrots, cucumber, daikon.\nSprinkle furikake and sesame seeds to finish.",
        yield_grams=900,
        company_id=poke_palace.id,
        created_by=evan.id,
        last_edited_by=evan.id,
    ),
])

# Recipes for Mesa Verde Kitchen
db.add_all([
    Recipe(
        title="Southwest Chicken Bowl",
        ingredients="280g grilled chicken breast, sliced\n250g Spanish rice\n120g black beans, drained\n100g roasted corn\n80g fire-roasted red peppers\n60g fresh pico de gallo\n50g sliced avocado\n40g cotija cheese, crumbled\n30g sour cream\n10g chipotle powder\n5g cumin\n5g smoked paprika\n15ml lime juice",
        instructions="Season chicken with chipotle powder, cumin, smoked paprika, salt, and pepper.\nGrill at 220°C for 6-7 min per side until internal temp reaches 74°C. Rest and slice.\nWarm black beans with a pinch of cumin and salt.\nRoast corn in a dry skillet over high heat until charred, about 4 min.\nLayer Spanish rice, then beans, chicken, corn, and peppers.\nFinish with pico de gallo, avocado, cotija, sour cream, and a squeeze of lime.",
        yield_grams=1028,
        company_id=mesa_verde.id,
        created_by=fiona.id,
        last_edited_by=fiona.id,
    ),
    Recipe(
        title="Greek Salad Bowl",
        ingredients="200g chopped romaine lettuce\n150g cherry tomatoes, halved\n120g cucumber, diced\n80g kalamata olives\n70g red onion, thinly sliced\n100g feta cheese, cubed\n60ml extra-virgin olive oil\n30ml red wine vinegar\n5g dried oregano\n3g salt\n2g black pepper\n100g pita chips",
        instructions="Whisk olive oil, red wine vinegar, oregano, salt, and pepper to make dressing.\nCombine romaine, tomatoes, cucumber, olives, and red onion in a large bowl.\nToss with dressing until evenly coated.\nTop with cubed feta — do not toss so it stays intact.\nServe with pita chips on the side or crumbled on top.",
        yield_grams=920,
        company_id=mesa_verde.id,
        created_by=fiona.id,
        last_edited_by=fiona.id,
    ),
    Recipe(
        title="Carne Asada Bowl",
        ingredients="300g skirt steak\n60ml orange juice\n30ml lime juice\n20ml soy sauce\n10g minced garlic\n5g cumin\n5g chili powder\n250g cilantro-lime rice\n100g pinto beans\n80g guacamole\n60g grilled onions and peppers\n40g salsa verde\n20g fresh cilantro",
        instructions="Combine orange juice, lime juice, soy sauce, garlic, cumin, and chili powder for marinade.\nMarinate skirt steak at least 2 hours, up to overnight in the refrigerator.\nGrill steak over very high heat 3-4 min per side for medium-rare. Rest 5 min, slice against the grain.\nWarm pinto beans with salt and a splash of the marinade.\nBuild bowl: rice, beans, sliced carne asada, grilled onions and peppers.\nTop with guacamole, salsa verde, and fresh cilantro.",
        yield_grams=960,
        company_id=mesa_verde.id,
        created_by=fiona.id,
        last_edited_by=fiona.id,
    ),
])

# Recipes for Harvest Table
db.add_all([
    Recipe(
        title="Autumn Grain Bowl",
        ingredients="200g farro, cooked\n150g roasted butternut squash, cubed\n100g roasted beets, quartered\n80g arugula\n60g candied pecans\n50g dried cranberries\n40g crumbled goat cheese\n60ml apple cider vinaigrette\n15ml olive oil\n5g fresh thyme\n3g salt\n2g black pepper",
        instructions="Cook farro per package instructions; season with salt and olive oil.\nToss butternut squash and beets separately with olive oil, salt, and thyme.\nRoast squash at 210°C for 25 min and beets for 35 min until tender.\nBuild bowl: warm farro as base, top with squash, beets, and arugula.\nAdd candied pecans, cranberries, and goat cheese.\nDrizzle apple cider vinaigrette just before serving.",
        yield_grams=845,
        company_id=harvest_table.id,
        created_by=grace.id,
        last_edited_by=grace.id,
    ),
    Recipe(
        title="Lemon Herb Quinoa Bowl",
        ingredients="220g quinoa, cooked\n150g roasted chickpeas\n120g baby spinach\n100g cherry tomatoes, halved\n80g cucumber, diced\n60g roasted red peppers\n50g hummus\n40g crumbled feta\n45ml lemon-tahini dressing\n10g fresh mint\n10g fresh dill\n5g lemon zest",
        instructions="Cook quinoa in vegetable broth for extra flavor; fluff and cool slightly.\nToss chickpeas with olive oil, cumin, smoked paprika, and salt; roast at 200°C for 30 min.\nWhisk together tahini, lemon juice, garlic, and water for dressing.\nArrange spinach and quinoa in bowl.\nAdd roasted chickpeas, tomatoes, cucumber, and red peppers.\nDollar hummus in the center, top with feta, fresh herbs, and lemon zest.\nFinish with lemon-tahini dressing.",
        yield_grams=870,
        company_id=harvest_table.id,
        created_by=grace.id,
        last_edited_by=grace.id,
    ),
    Recipe(
        title="Smashed Cucumber and Tofu Bowl",
        ingredients="250g extra-firm tofu, pressed\n300g jasmine rice, cooked\n200g Persian cucumbers\n30ml soy sauce\n20ml rice vinegar\n15ml chili oil\n10ml sesame oil\n8g sugar\n5g minced garlic\n5g grated ginger\n40g shelled edamame\n20g green onion, sliced\n10g toasted sesame seeds\n5g fresh cilantro",
        instructions="Press tofu 20 min; slice into planks and pan-fry in neutral oil until golden on each side, about 4 min per side.\nSmash cucumbers with the flat of a knife, tear into chunks, toss with rice vinegar, sugar, and a pinch of salt. Rest 10 min.\nWhisk soy sauce, chili oil, sesame oil, garlic, and ginger for the dressing.\nArrange rice in bowl, top with tofu and smashed cucumber.\nAdd edamame, drizzle dressing generously.\nTop with green onion, sesame seeds, and cilantro.",
        yield_grams=835,
        company_id=harvest_table.id,
        created_by=grace.id,
        last_edited_by=grace.id,
    ),
])

db.commit()
db.close()

print("Seeded successfully.")
print("  alice / password1  →  Acme Bakery")
print("  bob   / password2  →  Globex Foods")
print("  carol / password3  →  Acme Bakery + Globex Foods")
print("  diana / password4  →  The Bowl Co.")
print("  evan  / password5  →  Poke Palace")
print("  fiona / password6  →  Mesa Verde Kitchen")
print("  grace / password7  →  Harvest Table")
