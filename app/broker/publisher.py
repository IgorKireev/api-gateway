from faststream.rabbit import RabbitRouter, RabbitExchange, ExchangeType

from app.schemas.event_schema import OrderCreatedEvent


router = RabbitRouter()

orders_exchange = RabbitExchange(
    "orders",
    type=ExchangeType.FANOUT,
    durable=True,
)

order_created_publisher = router.publisher(exchange=orders_exchange)


async def publish_order_created(event: OrderCreatedEvent) -> None:
    await order_created_publisher.publish(event)
