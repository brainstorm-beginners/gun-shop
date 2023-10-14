from pydantic import BaseModel


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


class CategoryRead(BaseModel):
    name: str
    id: int

    class Config:
        extra = "allow"


class CategoryCreate(BaseModel):
    name: str
