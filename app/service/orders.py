import uuid
from sqlalchemy.exc import IntegrityError
from app.repository.orders import OrderRepository

from app.schemas.response_schema import OrderResponseSchema
from app.schemas.request_schema import OrderRequestSchema
from app.schemas.event_schema import OrderItemEvent, OrderCreatedEvent

from app.models.orders import Order, Customer, ShoppingAddress, Item
from app.exceptions import OrderCreationError, OrderNotFoundError
from app.mapper import to_order_response
from app.broker.publisher import publish_order_created


class OrderService:
    def __init__(self, order_repository: OrderRepository):
        self.repository = order_repository

    async def get_orders(self) -> list[OrderResponseSchema]:
        orders = await self.repository.get_orders()
        return [to_order_response(order) for order in orders]

    async def get_order(self, order_id: uuid.UUID) -> OrderResponseSchema:
        order = await self.repository.get_order(order_id)
        if not order:
            raise OrderNotFoundError
        return to_order_response(order)

    async def create(self, request: OrderRequestSchema) -> OrderResponseSchema | None:
        total_price = sum(item.price * item.quantity for item in request.items)
        try:
            customer = await self.repository.create_entity(
                Customer(
                    first_name=request.customer.first_name,
                    last_name=request.customer.last_name,
                    phone_number=request.customer.phone_number,
                    email=request.customer.email,
                )
            )

            address = await self.repository.create_entity(
                ShoppingAddress(
                    country=request.shipping_address.country,
                    city=request.shipping_address.city,
                    street=request.shipping_address.street,
                    postal_code=request.shipping_address.postal_code,
                )
            )

            order = await self.repository.create_entity(
                Order(
                    customer_id=customer.id,
                    shipping_address_id=address.id,
                    currency=request.currency,
                    total_price=total_price,
                    comment=request.comment,
                )
            )

            for item in request.items:
                await self.repository.create_entity(
                    Item(
                        order_id=order.id,
                        sku=item.sku,
                        quantity=item.quantity,
                        price=item.price,
                    )
                )

            await self.repository.commit()

            await publish_order_created(
                OrderCreatedEvent(
                    order_id=order.order_id,
                    total_price=total_price,
                    currency=request.currency,
                    customer_email=request.customer.email,
                    created_at=order.created_at,
                    items=[
                        OrderItemEvent(
                            sku=item.sku,
                            quantity=item.quantity,
                            price=item.price,
                        )
                        for item in request.items
                    ],
                )
            )
            return to_order_response(order)
        except IntegrityError:
            await self.repository.rollback()
            raise OrderCreationError
