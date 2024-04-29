from aiocouch import CouchDB

from src.core.settings import get_settings

settings = get_settings()

COUCHDB_URL = settings.COUCHDB_URL


async def get_couch_db_session() -> CouchDB:
    async with CouchDB(COUCHDB_URL) as client:
        yield client

