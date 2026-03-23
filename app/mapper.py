from app.schemas.response_schema import OrderResponseSchema
from app.models.orders import Order


def to_order_response(order: Order) -> OrderResponseSchema:
    return OrderResponseSchema(
        order_id=order.order_id,
        total_price=order.total_price,
        currency=order.currency,
        created_at=order.created_at,
        comment=order.comment,
    )
