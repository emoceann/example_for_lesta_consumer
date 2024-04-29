import pytest
from faststream.kafka import KafkaBroker
from aiocouch import Database, CouchDB


from src.consumer.schemas import LogDataSchema
from src.core.settings import get_settings

settings = get_settings()


@pytest.mark.asyncio(scope="session")
class TestKafkaBroker:
    async def test_couch_db_queue(self, test_broker: KafkaBroker, couch_session: CouchDB):
        test_data = LogDataSchema(partition="test", hello="hi")
        dump = test_data.model_dump(exclude={"ID"})
        await test_broker.publish(dump, settings.KAFKA_TOPIC_COUCHDB)

        db: Database = await couch_session[settings.COUCHDB_NAME]
        res = [i async for i in db.find(dump)]
        assert 'hello' in res[0]
