import pytest
from faststream.kafka import TestKafkaBroker
from aiocouch import CouchDB

from src.core.settings import get_settings
from src.server.kafka_app import create_kafka_app

settings = get_settings()


@pytest.fixture(scope="session")
async def test_broker():
    async with TestKafkaBroker(create_kafka_app()) as test_broker:
        yield test_broker


@pytest.fixture(scope="session")
async def couch_session() -> CouchDB:
    async with CouchDB(settings.COUCHDB_URL) as client:
        yield client
