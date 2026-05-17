from datetime import date

from src.exceptions import check_date_to_after_date_from, HotelNotFoundHTTPException, RoomNotFoundException, \
    HotelNotFoundException, ObjectNotFoundException
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import Room, RoomAddRequest, RoomAdd, RoomPatch, RoomPatchRequest
from src.services.base import BaseService
from src.services.hotels import HotelService


class RoomService(BaseService):
    async def get_filtered_by_time(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date,
    ):
        check_date_to_after_date_from(date_to=date_to, date_from=date_from)
        return await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

    async def get_room(self, hotel_id: int, room_id: int):
        room = await self.db.rooms.get_one_with_rels(id=room_id, hotel_id=hotel_id)
        if not room:
            raise RoomNotFoundException
        return room

    async def create_room(self, hotel_id: int, room_data: RoomAddRequest):
        await HotelService(self.db).get_hotel_exists_with_check(hotel_id=hotel_id)
        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        room = await self.db.rooms.add(data=_room_data)
        if room_data.facilities_ids:
            rooms_facilities_data = [
                RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids
            ]
            await self.db.rooms_facilities.add_bulk(rooms_facilities_data)
        await self.db.commit()
        return room

    async def edit_room(
            self,
            hotel_id: int,
            room_id: int,
            room_data: RoomAddRequest,
    ):
        await HotelService(self.db).get_hotel_exists_with_check(hotel_id=hotel_id)
        await self.get_room_exists_with_check(room_id=room_id)
        _room_data_dict = room_data.model_dump(exclude_unset=True)
        _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
        room = await self.db.rooms.edit(data=_room_data, hotel_id=hotel_id, id=room_id, exclude_unset=True)
        if "facilities_ids" in _room_data_dict:
            await self.db.rooms_facilities.set_room_facilities(
                room_id=room_id, facilities_ids=_room_data_dict["facilities_ids"]
            )
        await self.db.commit()
        return room


    async def partially_edit_room(
            self,
            hotel_id: int,
            room_id: int,
            room_data: RoomPatchRequest,
    ):
        await HotelService(self.db).get_hotel_exists_with_check(hotel_id=hotel_id)
        await self.get_room_exists_with_check(room_id=room_id)
        _room_data_dict = room_data.model_dump(exclude_unset=True)
        _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
        room = await self.db.rooms.edit(data=_room_data, hotel_id=hotel_id, id=room_id, exclude_unset=True)
        if "facilities_ids" in _room_data_dict:
            await self.db.rooms_facilities.set_room_facilities(
                room_id=room_id, facilities_ids=_room_data_dict["facilities_ids"]
            )
        await self.db.commit()
        return room

    async def delete_room(
            self,
            hotel_id: int,
            room_id: int,
    ):
        await HotelService(self.db).get_hotel_exists_with_check(hotel_id=hotel_id)
        await self.get_room_exists_with_check(room_id=room_id)
        result = await self.db.rooms.delete(hotel_id=hotel_id, id=room_id)
        return result


    async def get_room_exists_with_check(self, room_id: int) -> Room:
        try:
            return await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException