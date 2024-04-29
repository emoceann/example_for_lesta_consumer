import pytest
from aiocouch import Database

from src.consumer.repository.cdb_repository import LogCDBRepo
from src.consumer.schemas import LogDataSchema
from src.core.settings import get_settings


settings = get_settings()


@pytest.mark.asyncio(scope="session")
class TestLogController:
    @pytest.fixture
    def factory_repo(self, couch_session):
        return LogCDBRepo(couch_session)

    async def test_couchdb_handle_check(self, couch_session, factory_repo):
        log = LogDataSchema(partition="test", hello="hi")
        await factory_repo.insert_document(log, settings.COUCHDB_NAME)
        db: Database = await couch_session[settings.COUCHDB_NAME]
        res = await db.get(id=log.ID)
        assert 'hello' in res
