from faststream.rabbit import RabbitExchange, ExchangeType

from app.broker.broker import broker
from app.schemas.event_schema import OrderCreatedEvent


orders_exchange = RabbitExchange(
    "orders",
    type=ExchangeType.FANOUT,
    durable=True,
)

order_created_publisher = broker.publisher(exchange=orders_exchange)


async def publish_order_created(event: OrderCreatedEvent) -> None:
    await order_created_publisher.publish(event)
