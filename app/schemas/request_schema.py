from decimal import Decimal
from typing import Annotated, Literal

from pydantic import BaseModel, EmailStr, Field


class Item(BaseModel):
    sku: Annotated[str, Field(min_length=1, max_length=50)]
    quantity: Annotated[int, Field(ge=1, le=100)]
    price: Annotated[Decimal, Field(ge=0, decimal_places=2)]


class Customer(BaseModel):
    first_name: Annotated[str, Field(min_length=1, max_length=30)]
    last_name: Annotated[str, Field(min_length=1, max_length=30)]
    phone_number: Annotated[str, Field(pattern=r"^\+?[0-9]{10,15}$")]
    email: EmailStr


class ShoppingAddress(BaseModel):
    country: Annotated[str, Field(min_length=2, max_length=30)]
    city: Annotated[str, Field(min_length=2, max_length=30)]
    street: Annotated[str, Field(min_length=5, max_length=100)]
    postal_code: Annotated[str, Field(min_length=6, max_length=6)]


class OrderRequestSchema(BaseModel):
    customer: Customer
    shipping_address: ShoppingAddress
    items: Annotated[list[Item], Field(min_length=1)]
    currency: Literal["USD", "EUR", "RUB"]
    comment: Annotated[str, Field(max_length=100)]
