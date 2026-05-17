from src.api.dependencies import UserIdDep
from src.exceptions import ObjectNotFoundException, HotelNotFoundException
from src.schemas.booking import BookingAddRequest, BookingAdd
from src.services.base import BaseService
from src.services.hotels import HotelService
from src.services.rooms import RoomService


class BookingService(BaseService):
    async def get_bookings(self):
        booking = await self.db.bookings.get_all()
        return booking

    async def get_my_bookings(self, user_id: UserIdDep):
        booking = await self.db.bookings.get_filtered(user_id=user_id)
        return booking

    async def add_booking(
            self,
            user_id: UserIdDep,
            booking_data: BookingAddRequest
    ):
        room = await RoomService(self.db).get_room_exists_with_check(room_id=booking_data.room_id)
        hotel = await HotelService(self.db).get_hotel_exists_with_check(hotel_id=room.hotel_id)
        _booking_data = BookingAdd(user_id=user_id, price=room.price, **booking_data.model_dump())
        result = await self.db.bookings.add_booking(_booking_data, hotel_id=hotel.id) #AllRoomsAreBookedException
        await self.db.commit()
        return result