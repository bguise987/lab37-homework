"""
Tests that users cannot read or write recipes belonging to companies they
are not a member of.

Run from the repo root:
    pytest tests/backend/test_company_isolation.py -v
"""

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.insert(0, str(Path(__file__).parents[2] / "backend"))

import auth as auth_module
from database import Base, get_db
from main import app
from models import Company, Recipe, User

# ---------------------------------------------------------------------------
# In-memory database setup
# ---------------------------------------------------------------------------

TEST_DATABASE_URL = "sqlite:///:memory:"

# StaticPool forces all connections to reuse the same underlying SQLite
# connection, which is required for in-memory databases to be visible
# across the fixture's setup session and the TestClient's request sessions.
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def fresh_db():
    """Recreate all tables and seed minimal data before each test."""
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    db = TestingSessionLocal()

    acme = Company(name="Acme Bakery", address="1 Main St")
    globex = Company(name="Globex Foods", address="2 Industrial Ave")
    db.add_all([acme, globex])
    db.flush()

    alice = User(username="alice", password="pw")
    alice.company_ids = [acme.id]

    bob = User(username="bob", password="pw")
    bob.company_ids = [globex.id]

    db.add_all([alice, bob])
    db.flush()

    acme_recipe = Recipe(
        title="Acme Sourdough",
        ingredients="flour\nwater\nsalt",
        instructions="mix and bake",
        yield_grams=800,
        company_id=acme.id,
        created_by=alice.id,
        last_edited_by=alice.id,
    )
    globex_recipe = Recipe(
        title="Globex Tomato Sauce",
        ingredients="tomatoes\ngarlic",
        instructions="simmer",
        yield_grams=500,
        company_id=globex.id,
        created_by=bob.id,
        last_edited_by=bob.id,
    )
    db.add_all([acme_recipe, globex_recipe])
    db.commit()

    # Expose IDs for tests via module-level names that fixtures can reference
    fresh_db.acme_id = acme.id
    fresh_db.globex_id = globex.id
    fresh_db.alice_id = alice.id
    fresh_db.bob_id = bob.id
    fresh_db.acme_recipe_id = acme_recipe.id
    fresh_db.globex_recipe_id = globex_recipe.id

    db.close()

    # Clear any leftover sessions from previous tests
    auth_module.sessions.clear()

    yield

    auth_module.sessions.clear()


def token_for(username: str, password: str = "pw") -> str:
    resp = client.post("/api/auth/login", json={"username": username, "password": password})
    assert resp.status_code == 200, f"Login failed for {username}: {resp.text}"
    return resp.json()["token"]


def auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


# ---------------------------------------------------------------------------
# GET /api/recipes (list)
# ---------------------------------------------------------------------------


class TestListRecipes:
    def test_user_sees_only_own_company_recipes(self):
        token = token_for("alice")
        resp = client.get("/api/recipes", headers=auth(token))
        assert resp.status_code == 200
        titles = [r["title"] for r in resp.json()]
        assert "Acme Sourdough" in titles
        assert "Globex Tomato Sauce" not in titles

    def test_filter_by_own_company_allowed(self):
        token = token_for("alice")
        resp = client.get(f"/api/recipes?company_id={fresh_db.acme_id}", headers=auth(token))
        assert resp.status_code == 200

    def test_filter_by_foreign_company_forbidden(self):
        token = token_for("alice")
        resp = client.get(f"/api/recipes?company_id={fresh_db.globex_id}", headers=auth(token))
        assert resp.status_code == 403


# ---------------------------------------------------------------------------
# GET /api/recipes/{id}
# ---------------------------------------------------------------------------


class TestGetRecipe:
    def test_user_can_get_own_company_recipe(self):
        token = token_for("alice")
        resp = client.get(f"/api/recipes/{fresh_db.acme_recipe_id}", headers=auth(token))
        assert resp.status_code == 200
        assert resp.json()["title"] == "Acme Sourdough"

    def test_user_cannot_get_foreign_company_recipe(self):
        token = token_for("alice")
        resp = client.get(f"/api/recipes/{fresh_db.globex_recipe_id}", headers=auth(token))
        assert resp.status_code == 403

    def test_isolation_is_symmetric(self):
        """Bob also cannot read Acme's recipe."""
        token = token_for("bob")
        resp = client.get(f"/api/recipes/{fresh_db.acme_recipe_id}", headers=auth(token))
        assert resp.status_code == 403


# ---------------------------------------------------------------------------
# POST /api/recipes (create)
# ---------------------------------------------------------------------------


class TestCreateRecipe:
    RECIPE_BODY = {
        "title": "Test Recipe",
        "ingredients": "a\nb",
        "instructions": "do stuff",
        "yield_grams": 100,
    }

    def test_user_can_create_recipe_for_own_company(self):
        token = token_for("alice")
        body = {**self.RECIPE_BODY, "company_id": fresh_db.acme_id}
        resp = client.post("/api/recipes", json=body, headers=auth(token))
        assert resp.status_code == 201

    def test_user_cannot_create_recipe_for_foreign_company(self):
        token = token_for("alice")
        body = {**self.RECIPE_BODY, "company_id": fresh_db.globex_id}
        resp = client.post("/api/recipes", json=body, headers=auth(token))
        assert resp.status_code == 403


# ---------------------------------------------------------------------------
# PUT /api/recipes/{id} (update)
# ---------------------------------------------------------------------------


class TestUpdateRecipe:
    def test_user_can_update_own_company_recipe(self):
        token = token_for("alice")
        resp = client.put(
            f"/api/recipes/{fresh_db.acme_recipe_id}",
            json={"title": "Updated Sourdough"},
            headers=auth(token),
        )
        assert resp.status_code == 200
        assert resp.json()["title"] == "Updated Sourdough"

    def test_user_cannot_update_foreign_company_recipe(self):
        token = token_for("alice")
        resp = client.put(
            f"/api/recipes/{fresh_db.globex_recipe_id}",
            json={"title": "Hijacked"},
            headers=auth(token),
        )
        assert resp.status_code == 403


# ---------------------------------------------------------------------------
# DELETE /api/recipes/{id}
# ---------------------------------------------------------------------------


class TestDeleteRecipe:
    def test_user_can_delete_own_company_recipe(self):
        token = token_for("alice")
        resp = client.delete(f"/api/recipes/{fresh_db.acme_recipe_id}", headers=auth(token))
        assert resp.status_code == 204

    def test_user_cannot_delete_foreign_company_recipe(self):
        token = token_for("alice")
        resp = client.delete(f"/api/recipes/{fresh_db.globex_recipe_id}", headers=auth(token))
        assert resp.status_code == 403
