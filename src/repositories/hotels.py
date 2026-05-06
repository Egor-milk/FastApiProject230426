from datetime import date

from pydantic import BaseModel
from sqlalchemy import select

from src.database import engine
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_all(
            self,
            location,
            title,
            limit,
            offset,
    ) -> list[schema]:
            query = select(HotelsOrm)
            if location:
                query = query.filter(HotelsOrm.location.ilike(f"%{location.strip()}%"))
            if title:
                query = query.filter(HotelsOrm.title.ilike(f"%{title.strip()}%"))
            query = (
                query
                .limit(limit)
                .offset(offset)
            )
            #print(query.compile(engine, compile_kwargs={"literal_binds": True}))
            result = await self.session.execute(query) # stmt = statement это добавить, обновить или удалить, query для селектов
            #return  result.scalars().all()
            return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to)
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        print(rooms_ids_to_get.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        return await self.get_filtered(HotelsOrm.id.in_(hotels_ids_to_get))