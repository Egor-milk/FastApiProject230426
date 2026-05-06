from datetime import date

from pydantic import BaseModel
from sqlalchemy import select, func

from src.database import engine
from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            hotel_id: int,
    ):
        """
        WITH rooms_count as (
            SELECT room_id, count(*) as rooms_booked
            FROM bookings
            WHERE date_from <= '2026-01-01' AND date_to >= '2026-01-02'
            GROUP BY room_id
        ),
        rooms_left_table as (
            SELECT rooms.id as room_id, quantity, rooms_booked, quantity - coalesce(rooms_booked, 0) as rooms_left
            FROM rooms
            LEFT JOIN rooms_count on rooms.id = rooms_count.room_id
        )
        SELECT * FROM rooms_left_table
        WHERE rooms_left > 0
        ;
        """


        """
        sWITH rooms_count as (
            SELECT room_id, count(*) as rooms_booked
            FROM bookings
            WHERE date_from <= '2026-01-01' AND date_to >= '2026-01-02'
            GROUP BY room_id
        ),
        """
        rooms_count = (# сколько и каких комнат занято на определенный период (комната_id|количество бронирований)
            select(BookingsOrm.room_id, func.count("*").label("rooms_booked"))
            .select_from(BookingsOrm)
            .filter(
                BookingsOrm.date_from <= date_to,
                BookingsOrm.date_to >= date_from,
            )
            .group_by(BookingsOrm.room_id)
            .cte(name="rooms_count")
        )


        """
        srooms_left_table as (
            SELECT rooms.id as room_id, quantity, rooms_booked, quantity - coalesce(rooms_booked, 0) as rooms_left
            FROM rooms
            LEFT JOIN rooms_count on rooms.id = rooms_count.room_id
        ),
        """
        rooms_left_table = ( #таблица сколько комнат осталось незаняты room_id|какие-то данные|rooms_left
            select(
                RoomsOrm.id.label("room_id"),
                (RoomsOrm.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_left")
                #нужно обращаться через c так как не объект sqlalchemy
            )
            .select_from(RoomsOrm)
            .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id) #в sqlalchemy нет right join
            .cte(name="rooms_left_table") # CTE это типа WITH
        )

        """
        sSELECT * FROM rooms_left_table
        WHERE rooms_left > 0
        """
        rooms_ids_for_hotel = (
            select(RoomsOrm.id)
            .select_from(RoomsOrm)
            .filter_by(hotel_id=hotel_id)
            .subquery()
        )

        rooms_ids_to_get = (
            select(rooms_left_table.c.room_id)
            .select_from(rooms_left_table)
            .filter(
                rooms_left_table.c.rooms_left > 0,
                rooms_left_table.c.room_id.in_(rooms_ids_for_hotel) #подзапрос
            )
        )

        print(rooms_ids_to_get.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))