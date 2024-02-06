from pydantic import BaseModel, EmailStr

from src.schemas.base import SchemaBase


class UserBase(BaseModel):
    email: EmailStr
    name: str


class User(SchemaBase, UserBase):
    is_active: bool

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str
