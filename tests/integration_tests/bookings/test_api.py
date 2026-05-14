import pytest

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
        f"/bookings",
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