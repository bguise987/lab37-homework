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
db.add_all([acme, globex])
db.flush()

# Users
alice = User(username="alice", password="password1")
alice.company_ids = [acme.id]

bob = User(username="bob", password="password2")
bob.company_ids = [globex.id]

# User belonging to both companies
carol = User(username="carol", password="password3")
carol.company_ids = [acme.id, globex.id]

db.add_all([alice, bob, carol])
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

db.commit()
db.close()

print("Seeded successfully.")
print("  alice / password1  →  Acme Bakery")
print("  bob   / password2  →  Globex Foods")
print("  carol / password3  →  Acme Bakery + Globex Foods")
