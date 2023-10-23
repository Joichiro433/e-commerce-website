from typing import Optional

import ulid
from sqlmodel import Field, Relationship, SQLModel

from models.base_models import *


class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    email: str = Field(index=True)
    
    orders: list["Order"] = Relationship(back_populates="user")


class Order(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(ulid.new()), primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)

    user: Optional["User"] = Relationship(back_populates="orders")
    order_items: list["OrderItem"] = Relationship(back_populates="order")


class OrderItem(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(ulid.new()), primary_key=True)
    order_id: str = Field(foreign_key="order.id", index=True)
    product_id: str = Field(foreign_key="product.id", index=True)
    quantity: int

    order: Optional["Order"] = Relationship(back_populates="order_items")
    product: Optional["Product"] = Relationship(back_populates="order_items")


class Product(ProductBase, table=True):
    id: str = Field(primary_key=True)
    
    order_items: list["OrderItem"] = Relationship(back_populates="product")
