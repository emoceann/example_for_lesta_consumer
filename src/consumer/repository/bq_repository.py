from abc import ABC, abstractmethod

import httpx
from faststream import Depends

from src.core.utils import get_async_client, get_token
from src.consumer.schemas import LogDataSchema


class LogBQRepoAbstract(ABC):
    @abstractmethod
    async def write_log_in_big_query(self, data: LogDataSchema, url: str) -> None:
        raise NotImplementedError


class LogBQRepo(LogBQRepoAbstract):
    def __init__(
            self,
            client: httpx.AsyncClient = Depends(get_async_client),
            jwt_token: str = Depends(get_token)
    ):
        self.client = client
        self.api_token = jwt_token

    async def write_log_in_big_query(self, data: LogDataSchema, url: str) -> None:
        headers = {'Authorization': f'Bearer {self.api_token}'}
        response = await self.client.post(
            url,
            headers=headers,
            json={
                'rows': [
                    {
                        'json': data.model_dump(
                            mode='json',
                            exclude_none=True,
                        )
                    }
                ]
            }
        )
        response.raise_for_status()
