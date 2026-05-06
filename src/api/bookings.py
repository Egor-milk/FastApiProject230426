
from fastapi import Query, APIRouter, Body, HTTPException

from sqlalchemy.exc import MultipleResultsFound

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.booking import BookingAdd, Booking, BookingAddRequest
from src.schemas.rooms import Room
from src.services.auth import AuthService

router = APIRouter(prefix="/bookings", tags=["Бронирования"])

@router.get("")
async def get_bookings(
        db: DBDep,
):
    result = await db.bookings.get_all()
    return {"status": "ok", "data": result}

@router.get("/me")
async def get_my_bookings(
        db: DBDep,
        user_id: UserIdDep
):
    result = await db.bookings.get_filtered(user_id=user_id)
    return {"status": "ok", "data": result}

@router.post("")
async def bookings(
        db: DBDep,
        user_id: UserIdDep,
        booking_data: BookingAddRequest = Body(openapi_examples={
                '1': {
                    'summary': 'test_booking_1',
                    'value': {
                            "room_id": 27,
                            "date_from": "2026-01-01",
                            "date_to": "2026-01-11"
                      }
                },
                '2': {
                    'summary': 'dubai',
                    'value': {
                        "room_id": 28,
                        "date_from": "2026-02-01",
                        "date_to": "2026-02-11"
                      }
                }
            }),
):
    room: Room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    _booking_data = BookingAdd(
        user_id=user_id,
        price = room.price,
        **booking_data.model_dump()
    )
    result = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "ok", "data": result}
