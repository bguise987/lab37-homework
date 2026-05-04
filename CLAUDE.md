# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

A multi-company recipe management system built as a homework assignment for Lab37.

## Tech stack

- **Frontend**: Vue 3 + Vite + Vue Router + Pinia + Axios (`frontend/`)
- **Backend**: Python + FastAPI + SQLAlchemy (`backend/`)
- **Database**: SQLite (`backend/recipes.db`); PostgreSQL would be used in production

## Running the project

**Backend** (activate virtualenv first):
```bash
cd backend
python3 seed.py          # one-time: creates recipes.db with sample data
uvicorn main:app --reload --port 8000
```
API docs at http://localhost:8000/docs.

**Frontend:**
```bash
cd frontend
npm run dev              # http://localhost:5173
```
Vite proxies `/api` → `http://localhost:8000`, so no CORS setup needed in dev.

## Architecture

Three-tier web app: Vue 3 SPA → FastAPI REST backend → SQLite database.

### Key backend files

| File | Purpose |
|------|---------|
| `backend/main.py` | FastAPI app, CORS middleware, router registration |
| `backend/database.py` | SQLAlchemy engine + `get_db` dependency |
| `backend/models.py` | ORM models: `Company`, `User`, `Recipe` |
| `backend/schemas.py` | Pydantic request/response schemas |
| `backend/auth.py` | In-memory session store, `get_current_user` dependency, `require_company_access` |
| `backend/routes/auth.py` | `POST /api/auth/login`, `POST /api/auth/logout` |
| `backend/routes/recipes.py` | CRUD endpoints under `/api/recipes` |
| `backend/seed.py` | Populates DB with two companies, three users, sample recipes |

### Key frontend files

| File | Purpose |
|------|---------|
| `frontend/src/stores/auth.js` | Pinia store: token + userId, persisted to localStorage |
| `frontend/src/router/index.js` | Routes + auth guard |
| `frontend/src/views/LoginView.vue` | Login form |
| `frontend/src/views/DashboardView.vue` | Recipe list with client-side search |
| `frontend/src/views/RecipeView.vue` | Read-only recipe detail |
| `frontend/src/views/RecipeEditView.vue` | Create/edit form (also handles delete) |

### Database schema

- **Companies**: `id`, `name`, `address`
- **Users**: `id`, `username`, `password` (plaintext — MVP only), `company_ids` (JSON string), `created_at`, `last_login_at`
- **Recipes**: `id`, `title`, `ingredients` (newline-separated), `instructions` (newline-separated), `yield_grams`, `company_id` (FK), `created_by`, `last_edited_by`, `created_at`, `updated_at`

### Access control

Every recipe endpoint checks `recipe.company_id in user.company_ids` via `require_company_access()` in `backend/auth.py`. Violating this returns HTTP 403.

Auth uses a Bearer token in the `Authorization` header. The `get_current_user` FastAPI dependency validates it on every protected route.

## Known shortcuts (intentional MVP decisions)

- Passwords stored in plaintext
- In-memory session store (resets on server restart)
- Hard deletes on recipes
- No image support
- Yield info is static (no auto-recalculation)

## Tests

Two key test areas (TESTS.md):
1. Cross-company isolation — users must not access recipes from companies they don't belong to
2. Backend/database performance — maximum requests per second
