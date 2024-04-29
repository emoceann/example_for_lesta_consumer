from abc import ABC, abstractmethod

from faststream import Depends
from aiocouch import Database, CouchDB, Document

from src.consumer.schemas import LogDataSchema
from src.core.couch_db import get_couch_db_session


class LogCDBRepoAbstract(ABC):
    @abstractmethod
    async def insert_document(self, data: LogDataSchema, database_name: str) -> None:
        raise NotImplementedError


class LogCDBRepo(LogCDBRepoAbstract):
    def __init__(
            self,
            couch_db: CouchDB = Depends(get_couch_db_session)
    ):
        self.couch_db = couch_db

    async def insert_document(self, data: LogDataSchema, database_name: str) -> None:
        database: Database = await self.couch_db[database_name]
        doc: Document = await database.create(
            id=data.ID,
            data=data.model_dump(mode='json', exclude={"ID"}, exclude_none=True),
            exists_ok=True
        )
        await doc.save()
