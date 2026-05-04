# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

A multi-company recipe management system built as a homework assignment for Lab37. The codebase is currently in the design phase — the markdown files in the repo root document the planned architecture.

## Tech stack

- **Frontend**: Vue 3, served from a local dev server
- **Backend**: Python + FastAPI, served from a local dev server
- **Database**: SQLite (local/dev); PostgreSQL would be used in production

## Architecture

Three-tier web app: Vue 3 SPA → FastAPI REST backend → SQLite database.

### Database schema (planned)

- **Companies**: `id`, `name`, `address`
- **Users**: `id`, `username`, `password` (plaintext — MVP only), `company_ids`, `created_at` (UTC), `last_login_at` (UTC)
- **Recipes**: `id`, `ingredients` (newline-separated), `instructions` (newline-separated), `yield_grams`, `created_by_user_id`, `last_edited_by_user_id`, `company_id`

### Backend API endpoints (planned)

- `POST /login`, `POST /logout` — basic auth
- `GET /recipes?user_id=&company_id=` — list recipes filtered to companies the user belongs to
- `POST /recipes` — add recipe
- `PUT /recipes/{id}` — edit recipe
- `DELETE /recipes/{id}` — delete recipe

### Access control

Recipes are scoped to a company. Users belong to one or more companies and can only see/edit recipes for their associated companies. This must be enforced on every backend endpoint — see TESTS.md.

## Known shortcuts (intentional MVP decisions)

- Passwords stored in plaintext — explicitly noted as not production-ready
- Hard deletes on recipes (no soft-delete / recovery)
- No image support for recipes
- Yield info is static (no auto-recalculation when ingredients change)

## Tests

Two key test areas documented in TESTS.md:
1. Cross-company isolation — users must not access recipes from companies they don't belong to
2. Backend/database performance — maximum requests per second the stack can serve
