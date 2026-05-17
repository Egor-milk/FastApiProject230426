from datetime import date

from fastapi import APIRouter, Body, Query, HTTPException
from fastapi.openapi.models import Example

from src.api.dependencies import DBDep
from src.exceptions import check_date_to_after_date_from, ObjectNotFoundException, HotelNotFoundHTTPException, \
    RoomNotFoundHTTPException, RoomNotFoundException, HotelNotFoundException
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(default="2026-01-01"),
    date_to: date = Query(default="2026-02-01"),
):
    return await RoomService(db).get_filtered_by_time(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to
    )


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        return await RoomService(db).get_room(hotel_id=hotel_id, room_id=room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


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
        room = await RoomService(db).create_room(hotel_id=hotel_id, room_data=room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomAddRequest,
):
    room = await RoomService(db).edit_room(
        hotel_id=hotel_id,
        room_id=room_id,
        room_data=room_data,
    )
    return {"status": "OK", "data": room}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest,
):
    room = await RoomService(db).partially_edit_room(
        hotel_id=hotel_id,
        room_id=room_id,
        room_data=room_data,
    )
    return {"status": "OK", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
):
    try:
        result = await RoomService(db).delete_room(hotel_id=hotel_id, room_id=room_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException

    return {"status": "OK", "data": result}
