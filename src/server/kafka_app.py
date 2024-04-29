from faststream.kafka import KafkaBroker

from src.core.settings import get_settings
from src.consumer.routes import router as consumer_router

settings = get_settings()


def create_kafka_app() -> KafkaBroker:
    rabbit_broker = KafkaBroker(
        bootstrap_servers=settings.KAFKA_URL
    )

    # routers
    rabbit_broker.include_router(consumer_router)

    return rabbit_broker
