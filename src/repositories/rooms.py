from datetime import date

import sqlalchemy
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import NoResultFound


from src.database import engine
from src.exceptions import ObjectNotFoundException
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RoomDataMapper, RoomDataWithRelsMapper
from src.repositories.utils import rooms_ids_for_booking


class RoomsRepository(BaseRepository):
    model: RoomsOrm = RoomsOrm
    mapper = RoomDataMapper

    async def get_filtered_by_time(
        self,
        date_from: date,
        date_to: date,
        hotel_id,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        print(rooms_ids_to_get.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        query = (
            select(self.model) # type: ignore
            .options(
                selectinload(self.model.facilities) # type: ignore
            )  # помимо модели, через джоин подгрузи связь facilities
            .filter(RoomsOrm.id.in_(rooms_ids_to_get)) # type: ignore
        )

        result = await self.session.execute(query)
        return [
            RoomDataWithRelsMapper.map_to_domain_entity(model) for model in result.scalars().all()
        ]

    async def get_one_with_rels(self, **filter_by):
        query = (
            select(self.model).options(selectinload(self.model.facilities)).filter_by(**filter_by) # type: ignore
        )
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
        return RoomDataWithRelsMapper.map_to_domain_entity(model)
