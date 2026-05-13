import pytest

from src.config import settings
from src.database import Base, engine, engine_null_pull
from src.models import * #__init__.py

#session - сессия тестирования
@pytest.fixture(scope="session", autouse=True) #autouse - автоматический запуск кода при вызове pytest в консоли
async def async_main():
    print('я фикстура')
    assert settings.MODE == "TEST"
    async with engine_null_pull.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)