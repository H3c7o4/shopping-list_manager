import uuid

from fastapi_users import schemas
from pydantic import BaseModel


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass

class ShoppingListCreate(BaseModel):
    name: str
    owner_id: int

class ShoppingListRead(BaseModel):
    id: int
    name: str
    owner_id: int

class ItemCreate(BaseModel):
    name: str
    quantity: int
    unit_price: int
    shopping_list_id: int

class ItemRead(BaseModel):
    id: int
    name: str
    quantity: int
    unit_price: int
    shopping_list_id: int