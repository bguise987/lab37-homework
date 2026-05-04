from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from auth import get_current_user, require_company_access
from database import get_db
from models import Recipe, User
from schemas import RecipeCreate, RecipeResponse, RecipeUpdate

router = APIRouter(prefix="/api/recipes", tags=["recipes"])


@router.get("", response_model=list[RecipeResponse])
def list_recipes(
    company_id: int | None = Query(default=None),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if company_id is not None:
        require_company_access(user, company_id)
        return db.query(Recipe).filter(Recipe.company_id == company_id).all()
    return db.query(Recipe).filter(Recipe.company_id.in_(user.company_ids)).all()


@router.post("", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED)
def create_recipe(
    body: RecipeCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    require_company_access(user, body.company_id)
    recipe = Recipe(
        title=body.title,
        ingredients=body.ingredients,
        instructions=body.instructions,
        yield_grams=body.yield_grams,
        company_id=body.company_id,
        created_by=user.id,
        last_edited_by=user.id,
    )
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe


@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe(
    recipe_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    recipe = _get_accessible_recipe(recipe_id, user, db)
    return recipe


@router.put("/{recipe_id}", response_model=RecipeResponse)
def update_recipe(
    recipe_id: int,
    body: RecipeUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    recipe = _get_accessible_recipe(recipe_id, user, db)
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(recipe, field, value)
    recipe.last_edited_by = user.id
    recipe.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(recipe)
    return recipe


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(
    recipe_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    recipe = _get_accessible_recipe(recipe_id, user, db)
    db.delete(recipe)
    db.commit()


def _get_accessible_recipe(recipe_id: int, user: User, db: Session) -> Recipe:
    recipe = db.get(Recipe, recipe_id)
    if recipe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    require_company_access(user, recipe.company_id)
    return recipe
