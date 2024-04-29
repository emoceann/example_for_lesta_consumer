import sys
from functools import lru_cache

from pydantic import FilePath
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # kafka
    KAFKA_URL: str
    KAFKA_TOPIC_COUCHDB: str
    KAFKA_TOPIC_BIGQUERY: str

    # couch_db
    COUCHDB_URL: str
    COUCHDB_NAME: str

    # big_query
    BIG_QUERY_PROJECT_ID: str
    BIG_QUERY_DATASET_ID: str
    BIG_QUERY_TABLE_ID: str

    GOOGLE_SERVICE_JSON_PATH: FilePath


class TestSettings(Settings):
    model_config = SettingsConfigDict(env_file="test.env")


@lru_cache
def get_settings() -> Settings | TestSettings:
    if "pytest" in sys.modules:
        return TestSettings()
    return Settings()
