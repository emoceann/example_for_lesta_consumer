from faststream import FastStream

from src.server.kafka_app import create_kafka_app


def create_app() -> FastStream:
    factory_app = FastStream(broker=create_kafka_app())
    return factory_app


app = create_app()
