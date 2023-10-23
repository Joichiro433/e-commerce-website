from datetime import datetime

from sqlmodel import SQLModel

from models.base_models import *
from models.table_models import *


class Message(SQLModel):
    message: str


class SignUpCreate(SQLModel):
    email: str
    password: str


class UserRead(SQLModel):
    id: str
    email: str


class OrderItemCreate(SQLModel):
    product_id: str
    quantity: int


class ProductRead(ProductBase):
    id: str


class ProductCount(SQLModel):
    count: int


class OrderItemRead(SQLModel):
    quantity: int
    product: ProductRead


class OrderRead(SQLModel):
    id: str
    order_items: list[OrderItemRead]
    purchase_date: datetime


class UserOrderRead(SQLModel):
    id: str
    email: str
    orders: list[OrderRead]
