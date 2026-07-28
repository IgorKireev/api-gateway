from faststream.rabbit import RabbitBroker
from app.settings import settings
from app.broker.publisher import router as orders_router


broker = RabbitBroker(settings.rabbitmq_url)
broker.include_router(orders_router)
