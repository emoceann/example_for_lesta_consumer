import pytest
from aiocouch import Database

from src.consumer.controller import LogController
from src.consumer.repository.cdb_repository import LogCDBRepo
from src.consumer.schemas import LogDataSchema
from src.core.settings import get_settings

settings = get_settings()


@pytest.mark.asyncio(scope="session")
class TestLogController:
    @pytest.fixture
    def factory_controller(self, couch_session):
        return LogController(log_cdb_repo=LogCDBRepo(couch_session))

    async def test_couchdb_handle(self, couch_session, factory_controller):
        log = LogDataSchema(partition="test", hello="hi")
        await factory_controller.write_log_in_couchdb(log)
        db: Database = await couch_session[settings.COUCHDB_NAME]
        res = await db.get(id=log.ID)
        assert 'hello' in res
