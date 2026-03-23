from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict
from pydantic.types import UUID4


class OrderResponseSchema(BaseModel):
    order_id: UUID4
    total_price: Decimal
    currency: Literal["USD", "EUR", "RUB"]
    created_at: datetime
    comment: str

    model_config = ConfigDict(from_attributes=True)