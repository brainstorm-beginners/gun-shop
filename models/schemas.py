from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, Field

from models.models import Gun


class GunRead(BaseModel):
    name: str
    barrel_type: str
    caliber: str
    price: float
    category_id: int

    class Config:
        orm_mode = True
        extra = "allow"


class GunCreate(BaseModel):
    name: str
    barrel_type: str
    caliber: str
    price: float
    category_id: int


class GunFilter(Filter):
    name__in: Optional[list[str]] = Field(alias="names")
    barrel_type__in: Optional[list[str]] = Field(alias="barrelTypes")
    caliber__in: Optional[list[str]] = Field(alias="calibers")
    category_id__in: Optional[list[int]] = Field(alias="categories")

    class Constants(Filter.Constants):
        model = Gun

    class Config:
        allow_population_by_field_name = True


class CategoryRead(BaseModel):
    name: str
    id: int

    class Config:
        extra = "allow"


class CategoryCreate(BaseModel):
    name: str
