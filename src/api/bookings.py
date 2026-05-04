
from fastapi import Query, APIRouter, Body, HTTPException

from sqlalchemy.exc import MultipleResultsFound

from src.api.dependencies import DBDep
from src.schemas.booking import BookingAdd, Booking, BookingAddRequest

router = APIRouter(prefix="/bookings", tags=["Бронирования"])

@router.post('/bookings')
async def bookings(
        db: DBDep,
        booking_data: BookingAddRequest = Body(openapi_examples={
                '1': {
                    'summary': 'test_booking_1',
                    'value': {
                            "user_id": 9,
                            "room_id": 27,
                            "date_from": "2026-01-01",
                            "date_to": "2026-01-11",
                            "price": 0
                      }
                },
                '2': {
                    'summary': 'dubai',
                    'value': {
                        "user_id": 12,
                        "room_id": 28,
                        "date_from": "2026-02-01",
                        "date_to": "2026-02-11",
                        "price": 0
                      }
                }
            }),
):
    _booking_data = BookingAdd(price=0,**booking_data.model_dump())
    result = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "ok", "data": result}
