from faststream import Depends
from faststream.kafka import KafkaRouter

from src.core.settings import get_settings
from src.consumer.controller import LogController
from src.consumer.schemas import LogDataSchema


router = KafkaRouter()
settings = get_settings()


@router.subscriber(settings.KAFKA_TOPIC_COUCHDB)
async def couchdb_log_queue(
        data: LogDataSchema,
        controller: LogController = Depends(LogController)
):
    return await controller.write_log_in_couchdb(data)


@router.subscriber(settings.KAFKA_TOPIC_BIGQUERY)
async def bigquery_log_queue(
        data: LogDataSchema,
        controller: LogController = Depends(LogController)
):
    return await controller.write_log_in_bigquery(data)
