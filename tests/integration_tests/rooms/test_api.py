import pytest

from src.schemas.rooms import RoomAddRequest


@pytest.mark.parametrize(
    "hotel_id, room_data, status_code",
    [
        (
                1,
                RoomAddRequest(
                    title= "luxe_1",
                    description= "very luxe room",
                    price= 10000,
                    quantity= 1,
                    facilities_ids= [],
                ),
                200
        ),
    ],
)
async def test_create_and_get_rooms(ac, hotel_id, room_data, status_code):
    response = await ac.post(
        f"/hotels/{hotel_id}/rooms",
        json={
            "title": room_data.title,
            "description": room_data.description,
            "price": room_data.price,
            "quantity": room_data.quantity,
            "facilities_ids": room_data.facilities_ids,
        },
    )
    assert response.status_code == status_code

    #get_response = await ac.get(f"/hotels/{hotel_id}/rooms") #ВОЗЬМИ АЙДИ И ПРОВЕРЬ



@pytest.mark.parametrize(
    "hotel_id, date_from, date_to, status_code",
    [
        (1, "2026-04-01", "2026-05-01", 200),
    ],
)
async def test_get_rooms(authenticated_ac, hotel_id, date_from, date_to, status_code):
    response = await authenticated_ac.get(
        f"/hotels/{hotel_id}/rooms",
        params={
            "date_from": "2026-05-01",
            "date_to": "2026-05-02",
        },
    )
    print(f"{response.json()=}")

    assert response.status_code == 200
