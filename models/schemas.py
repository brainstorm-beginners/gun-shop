from pydantic import BaseModel


from pydantic import BaseModel
from typing import List, Optional


class GunBase(BaseModel):
    name: str
    barrel_type: str
    caliber: str
    price: float


class GunCreate(GunBase):
    pass


class GunUpdate(GunBase):
    pass


class GunInDBBase(GunBase):
    id: int
    category_id: int

    class Config:
        orm_mode = True


class Gun(GunInDBBase):
    pass


class GunInDB(GunInDBBase):
    pass


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryInDBBase(CategoryBase):
    id: int

    class Config:
        orm_mode = True


class Category(CategoryInDBBase):
    pass


class CategoryInDB(CategoryInDBBase):
    guns: List[Gun] = []

