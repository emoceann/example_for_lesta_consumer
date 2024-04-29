import httpx
from google.auth import jwt
from faststream import ContextRepo, Context, apply_types

from src.core.settings import get_settings

settings = get_settings()


async def get_async_client() -> httpx.AsyncClient:
    async with httpx.AsyncClient() as client:
        yield client


@apply_types
def get_token(
        context: ContextRepo,
        creds: jwt.Credentials = Context(
            "creds",
            default=jwt.Credentials.from_service_account_file(
                settings.GOOGLE_SERVICE_JSON_PATH,
                audience='https://bigquery.googleapis.com/')
        )
):
    if creds and creds.valid:
        return creds.token[0].decode()
    creds.token = creds._make_jwt()
    context.set_global('creds', creds)
    return creds.token[0].decode()
