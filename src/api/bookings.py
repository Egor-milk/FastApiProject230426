from fastapi import APIRouter, Body, HTTPException
from fastapi.openapi.models import Example


from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException, RoomNotFoundHTTPException, \
    RoomNotFoundException, HotelNotFoundException, HotelNotFoundHTTPException, AllRoomsAreBookedHTTPException
from src.schemas.booking import BookingAdd, BookingAddRequest
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("")
async def get_bookings(
    db: DBDep,
):
    booking = await BookingService(db).get_bookings()
    return {"status": "ok", "data": booking}


@router.get("/me")
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    booking = await BookingService(db).get_my_bookings(user_id=user_id)
    return {"status": "ok", "data": booking}


@router.post("")
async def add_booking(
    db: DBDep,
    user_id: UserIdDep,
    booking_data: BookingAddRequest = Body(
        openapi_examples={
            "1": Example(
                summary="test_booking_1",
                value={"room_id": 34, "date_from": "2026-01-01", "date_to": "2026-02-01"},
            ),
            "2": Example(
                summary="dubai",
                value={"room_id": 28, "date_from": "2026-01-01", "date_to": "2026-02-01"},
            ),
        }
    ),
):
    try:
        result = await BookingService(db).add_booking(user_id=user_id, booking_data=booking_data)
    except RoomNotFoundException as ex:
        raise RoomNotFoundHTTPException from ex
    except HotelNotFoundException as ex:
        raise HotelNotFoundHTTPException from ex
    except AllRoomsAreBookedException as ex:
        raise AllRoomsAreBookedHTTPException from ex
    return {"status": "ok", "data": result}
