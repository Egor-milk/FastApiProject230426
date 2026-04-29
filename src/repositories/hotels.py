from sqlalchemy import select

from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
            self,
            location,
            title,
            limit,
            offset,
    ) -> HotelsOrm:
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
            return  result.scalars().all()