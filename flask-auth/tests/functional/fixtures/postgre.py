import pytest_asyncio
from sqlalchemy import create_engine
from settings import postgre_settings
from utils.helpers import conn_context


async def _delete_data_from_postgre(engine):
    with conn_context(engine.raw_connection()) as conn, conn.cursor() as cursor:
        cursor.execute("delete from users;")
        cursor.execute("delete from user_actions_history;")
        conn.commit()


@pytest_asyncio.fixture(scope="function")
async def postgre_engine():
    engine = create_engine(postgre_settings.get_db_uri())
    yield engine
    _delete_data_from_postgre(engine)
