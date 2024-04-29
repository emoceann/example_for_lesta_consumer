from faststream import Depends

from src.consumer.repository.bq_repository import LogBQRepo
from src.consumer.repository.cdb_repository import LogCDBRepo
from src.consumer.schemas import LogDataSchema
from src.core.settings import get_settings


settings = get_settings()


class LogController:
    big_query_url = (f"https://bigquery.googleapis.com/bigquery/v2/projects/"
                     f"{settings.BIG_QUERY_PROJECT_ID}"
                     f"/datasets/{settings.BIG_QUERY_DATASET_ID}"
                     f"/tables/{settings.BIG_QUERY_TABLE_ID}"
                     f"/insertAll")
    cdb_database_name = settings.COUCHDB_NAME

    def __init__(
            self,
            log_cdb_repo: LogCDBRepo = Depends(LogCDBRepo),
            log_bq_repo: LogBQRepo = Depends(LogBQRepo)
    ):
        self.log_cdb_repo = log_cdb_repo
        self.log_bq_repo = log_bq_repo

    async def write_log_in_couchdb(self, data: LogDataSchema) -> None:
        await self.log_cdb_repo.insert_document(data, self.cdb_database_name)

    async def write_log_in_bigquery(self, data: LogDataSchema) -> None:
        await self.log_bq_repo.write_log_in_big_query(
            data,
            self.big_query_url
        )
