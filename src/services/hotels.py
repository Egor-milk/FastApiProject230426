from datetime import date

from sqlalchemy.ext.asyncio import result

from src.exceptions import check_date_to_after_date_from, ObjectNotFoundException, HotelNotFoundException
from src.schemas.hotels import Hotel, HotelAdd, HotelPatch
from src.services.base import BaseService


class HotelService(BaseService):
    async def get_filtered_by_time(
            self,
            pagination, #: PaginationDep,
            title: str | None,
            location: str | None,
            date_from: date,
            date_to: date,
    ) -> list[Hotel]:
        check_date_to_after_date_from(date_to=date_to, date_from=date_from)
        per_page = pagination.per_page or 5
        return await self.db.hotels.get_filtered_by_time(
            location=location,
            title=title,
            date_from=date_from,
            date_to=date_to,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )

    async def get_hotel(self, hotel_id):
        return await self.db.hotels.get_one(id=hotel_id)

    async def add_hotel(self, data: HotelAdd):
        hotel = await self.db.hotels.add(data=data)
        await self.db.commit()
        return hotel

    async def edit_hotel(self, hotel_id: int, data: HotelAdd):
        hotel = await self.db.hotels.edit(data=data, id=hotel_id)
        await self.db.commit()
        return hotel

    async def edit_hotel_partially(self, hotel_id: int, data: HotelPatch, exclude_unset: bool = False):
        hotel = await self.db.hotels.edit(data=data, exclude_unset=exclude_unset, id=hotel_id)
        await self.db.commit()
        return hotel

    async def get_hotel_exists_with_check(self, hotel_id: int) -> Hotel:
        try:
            return await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException