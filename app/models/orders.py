import uuid
from decimal import Decimal
from datetime import datetime

from sqlalchemy import Numeric, String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Customer(Base):
    __tablename__ = "customers"

    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    phone_number: Mapped[str] = mapped_column(String(15))
    email: Mapped[str] = mapped_column(String(255))


class ShoppingAddress(Base):
    __tablename__ = "shopping_addresses"

    country: Mapped[str] = mapped_column(String(30))
    city: Mapped[str] = mapped_column(String(50))
    street: Mapped[str] = mapped_column(String(100))
    postal_code: Mapped[str] = mapped_column(String(6))


class Order(Base):
    __tablename__ = "orders"

    order_id: Mapped[uuid.UUID] = mapped_column(unique=True, default=uuid.uuid4)
    total_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    currency: Mapped[str] = mapped_column(String(3))
    comment: Mapped[str] = mapped_column(String(100), default="")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="CASCADE")
    )
    shipping_address_id: Mapped[int] = mapped_column(
        ForeignKey("shopping_addresses.id", ondelete="CASCADE")
    )


class Item(Base):
    __tablename__ = "items"

    sku: Mapped[str] = mapped_column(String(50))
    quantity: Mapped[int] = mapped_column()
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
