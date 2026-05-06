from datetime import date

from fastapi import APIRouter, Body, HTTPException, Query

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch

router = APIRouter(prefix='/hotels', tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        db: DBDep,
        hotel_id: int,
        date_from: date = Query(example="2026-01-01"),
        date_to: date = Query(example="2026-02-01"),
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

# @router.get("/{hotel_id}/rooms")
# async def get_rooms(
#         db: DBDep,
#         hotel_id: int,
# ):
#     return await db.rooms.get_filtered(hotel_id=hotel_id)
@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(
        db: DBDep,
        hotel_id: int,
        room_id: int
):
        return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)



@router.post("/{hotel_id}/rooms")
async def create_rooms(
        db: DBDep,
        hotel_id: int,
        room_data: RoomAddRequest = Body(
            openapi_examples={
                "1": {
                    "summary": "test_room_1",
                    "value": {
                        "title": "luxe_1",
                        "description": "very luxe room",
                        "price": 10000,
                        "quantity": 1,
                    }
                },
                "2": {
                    "summary": "test_room_2",
                    "value": {
                        "title": "econom",
                        "description": "low price room",
                        "price": 100,
                        "quantity": 10,
                    }
                }
            })
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(data=_room_data)
    await db.commit()
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomAddRequest,
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    result = await db.rooms.edit(data=_room_data, id=room_id)
    await db.commit()
    return {"status": "OK", "data": result}

@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest,
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    result = await db.rooms.edit(
        data=_room_data,
        hotel_id=hotel_id,
        id=room_id,
        exclude_unset=True
    )
    return {"status": "OK", "data": result}



@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
):
    result = await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    return {"status": "OK", "data": result}