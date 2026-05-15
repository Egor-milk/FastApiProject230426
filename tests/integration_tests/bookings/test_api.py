import pytest

from tests.conftest import get_db_null_pool


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2026-01-01", "2026-02-01", 200),
    (1, "2026-01-01", "2026-02-01", 200),
    (1, "2026-01-01", "2026-02-01", 200),
    (1, "2026-01-01", "2026-02-01", 200),
    (1, "2026-01-01", "2026-02-01", 200),
    (1, "2026-01-01", "2026-02-01", 409),
    (1, "2026-01-01", "2026-02-01", 409),
    (1, "2026-01-01", "2026-02-01", 409),
    (1, "2026-01-01", "2026-02-01", 409),
    (1, "2026-01-01", "2026-02-01", 409),
])
async def test_add_booking(
        room_id, date_from, date_to, status_code,
        db, authenticated_ac):
    #room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "ok"
        assert "data" in res


@pytest.fixture(scope='module')
async def delete_all_bookings():
    async for _db in get_db_null_pool():
        await _db.bookings.delete_all_bookings()
        await _db.commit()


@pytest.mark.parametrize("room_id, date_from, date_to, status_code, count_of_bookings",[
    (1, "2026-01-01", "2026-02-01", 200, 1),
    (1, "2026-01-01", "2026-02-01", 200, 2),
    (1, "2026-01-01", "2026-02-01", 200, 3),
])
async def test_add_and_get_bookings(
        room_id, date_from, date_to, status_code, count_of_bookings,
        delete_all_bookings, authenticated_ac
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    assert response.status_code == status_code
    get_response = await authenticated_ac.get(
        "/bookings/me",
    )
    assert get_response.status_code == status_code
    assert len(get_response.json()["data"]) == count_of_bookings