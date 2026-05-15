from datetime import date

from fastapi import HTTPException
from sqlalchemy import select, delete

from src.database import engine
from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.booking import BookingAdd



class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = (
            select(BookingsOrm)
            .filter(BookingsOrm.date_from == date.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]


    async def add_booking(self, booking_data: BookingAdd, hotel_id: int):

        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=booking_data.date_from,
            date_to=booking_data.date_to,
            hotel_id=hotel_id)

        rooms_ids_to_book_res = await self.session.execute(rooms_ids_to_get)
        rooms_ids_to_book: list[int] = rooms_ids_to_book_res.scalars().all()

        if booking_data.room_id in rooms_ids_to_book:
            new_booking = await self.add(booking_data)
            return new_booking
        else:
            raise HTTPException(status_code=409)

    async def delete_all_bookings(self):
        query = delete(BookingsOrm)
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        await self.session.execute(query)
