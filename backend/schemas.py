from datetime import datetime

from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class CompanyInfo(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class LoginResponse(BaseModel):
    token: str
    user_id: int
    companies: list[CompanyInfo]


class RecipeBase(BaseModel):
    title: str
    ingredients: str
    instructions: str
    yield_grams: float | None = None
    company_id: int


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(BaseModel):
    title: str | None = None
    ingredients: str | None = None
    instructions: str | None = None
    yield_grams: float | None = None


class RecipeResponse(RecipeBase):
    id: int
    created_by: int
    last_edited_by: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
