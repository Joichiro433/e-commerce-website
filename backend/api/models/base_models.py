from typing import Optional

from sqlmodel import SQLModel


class AuthBase(SQLModel):
    email: str
    password: str


class ProductBase(SQLModel):
    name: str
    description: Optional[str] = None
    price: float
    author: str
    image_url: str