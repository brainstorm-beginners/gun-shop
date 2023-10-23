from datetime import date
from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import BaseModel, Field
from sqlalchemy import or_
from sqlalchemy.sql.expression import and_

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

    def get_filter_criteria(self) -> and_:
        criteria = []
        if self.name__in:
            name_criteria = or_(Gun.name.in_(self.name__in), Gun.name.like("%{}%".format(self.name__in[0])))
            criteria.append(name_criteria)
        if self.barrel_type__in:
            criteria.append(Gun.barrel_type.in_(self.barrel_type__in))
        if self.caliber__in:
            criteria.append(Gun.caliber.in_(self.caliber__in))
        if self.category_id__in:
            criteria.append(Gun.category_id.in_(self.category_id__in))
        return and_(*criteria)

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


class AmmoRead(BaseModel):
    calibers: str
    amount: int


class AmmoCreate(AmmoRead):
    pass

