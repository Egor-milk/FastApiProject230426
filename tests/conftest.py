# ruff: noqa: E402
import json
from unittest import mock


def empty_cache(*args, **kwargs):
    def wrapper(func):
        return func

    return wrapper


mock.patch("fastapi_cache.decorator.cache", empty_cache).start()

import pytest

from src.api.dependencies import get_db
from src.config import settings
from src.database import Base, engine_null_pool
from src.main import app
from src.models import *  # noqa
from src.database import async_session_maker_null_pool

from httpx import AsyncClient, ASGITransport

from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool() -> DBManager:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="function")
async def db() -> DBManager:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


# session - сессия тестирования
@pytest.fixture(
    scope="session", autouse=True
)  # autouse - автоматический запуск кода при вызове pytest в консоли
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/mock_hotels.json", encoding="utf-8") as file_hotels:
        hotels = json.load(file_hotels)
    with open("tests/mock_rooms.json", encoding="utf-8") as file_rooms:
        rooms = json.load(file_rooms)

    hotels = [HotelAdd.model_validate(hotel) for hotel in hotels]
    rooms = [RoomAdd.model_validate(room) for room in rooms]

    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(ac, setup_database):
    await ac.post(
        "/auth/register",
        json={
            "email": "test@mail.ru",
            "password": "1234",
        },
    )


@pytest.fixture(scope="session")
async def authenticated_ac(register_user, ac):
    await ac.post(
        "/auth/login",
        json={
            "email": "test@mail.ru",
            "password": "1234",
        },
    )
    assert ac.cookies["access_token"]
    print(f"cookies: {ac.cookies}")
    yield ac


# pytest -v -s


# transport = ASGITransport(app=app1)
# with open('tests/mock_hotels.json', 'rb') as f:
#     json_data = json.load(f)
# async with AsyncClient(transport=transport, base_url="http://test") as ac:
#     for i in json_data:
#         await ac.post(
#             "/hotels",
#             json=i
#         )
#
# with open('tests/mock_rooms.json', 'rb') as f:
#     json_data = json.load(f)
# async with AsyncClient(transport=transport, base_url="http://test") as ac:
#     for number, values in enumerate(json_data):
#         await ac.post(
#             f"hotels/{values['hotel_id']}/rooms",
#             json={
#                 "title": f"{values['title']}",
#                 "description": f"{values['description']}",
#                 "price": f"{values['price']}",
#                 "quantity": f"{values['quantity']}"
#             }
#         )
