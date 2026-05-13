import pytest

from src.config import settings
from src.database import Base, engine_null_pull
from src.main import app as app1
from src.models import * #__init__.py

from httpx import AsyncClient, ASGITransport


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"

#session - сессия тестирования
@pytest.fixture(scope="session", autouse=True) #autouse - автоматический запуск кода при вызове pytest в консоли
async def setup_database(check_test_mode):
    async with engine_null_pull.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):
    transport = ASGITransport(app=app1)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post(
            "/auth/register",
            json={
                "email": "test@mail.ru",
                "password": "1234",
            }
        )




# pytest -v -s