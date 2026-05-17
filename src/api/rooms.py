from datetime import date

from fastapi import APIRouter, Body, Query
from fastapi.openapi.models import Example

from src.api.dependencies import DBDep
from src.exceptions import check_date_to_after_date_from, ObjectNotFoundException, HotelNotFoundException, \
    RoomNotFoundException
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(default="2026-01-01"),
    date_to: date = Query(default="2026-02-01"),
):
    check_date_to_after_date_from(date_to=date_to, date_from=date_from)
    return await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    room = await db.rooms.get_one_or_none_with_rels(id=room_id, hotel_id=hotel_id)
    if not room:
        raise HotelNotFoundException


@router.post("/{hotel_id}/rooms")
async def create_rooms(
    db: DBDep,
    hotel_id: int,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "1": Example(
                summary="test_room_1",
                value={
                    "title": "luxe_1",
                    "description": "very luxe room",
                    "price": 10000,
                    "quantity": 1,
                    "facilities_ids": [1, 2],
                },
            ),
            "2": Example(
                summary="test_room_2",
                value={
                    "title": "econom",
                    "description": "low price room",
                    "price": 100,
                    "quantity": 10,
                    "facilities_ids": [1, 2],
                },
            ),
        }
    ),
):
    try:
        await db.hotels.get_one(hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundException

    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(data=_room_data)
    if room_data.facilities_ids:
        rooms_facilities_data = [
            RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids
        ]
        await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomAddRequest,
):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundException
    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundException

    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.edit(data=_room_data, id=room_id)
    await db.rooms_facilities.set_room_facilities(
        room_id=room_id, facilities_ids=room_data.facilities_ids
    )
    await db.commit()
    return {"status": "OK", "data": room}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest,
):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundException
    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundException
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
    room = await db.rooms.edit(data=_room_data, hotel_id=hotel_id, id=room_id, exclude_unset=True)
    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(
            room_id=room_id, facilities_ids=_room_data_dict["facilities_ids"]
        )
    await db.commit()
    return {"status": "OK", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundException
    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundException
    result = await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    return {"status": "OK", "data": result}
