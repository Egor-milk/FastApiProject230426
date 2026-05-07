from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete

from src.database import engine
from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel):
        add_hotel_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True})) # показывает данные которые отправляются в бд
        hotel = await self.session.execute(add_hotel_stmt)
        model = hotel.scalars().one()
        return self.mapper.map_to_domain_entity(model)

    async def add_bulk(self, data: list[BaseModel]): #bulk - много данных
        add_hotel_stmt = insert(self.model).values([item.model_dump() for item in data])

        await self.session.execute(add_hotel_stmt)


    async def edit(self, data: BaseModel, exclude_unset: bool=False, **filter_by):
        edit_hotel_stmt = (update(self.model)
                           .filter_by(**filter_by)
                           .values(**data.model_dump(exclude_unset=exclude_unset))
                           .returning(self.model))
        #exclude_unset=True позволяет не вставлять не переданные параметры
        print(edit_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        hotel = await self.session.execute(edit_hotel_stmt)
        model = hotel.scalars().one()
        return self.mapper.map_to_domain_entity(model)

    async def delete(self, **filter_by):
        delete_hotel_stmt = delete(self.model).filter_by(**filter_by).returning(self.model)
        print(delete_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        hotel = await self.session.execute(delete_hotel_stmt)
        model = hotel.scalars().one()
        return self.mapper.map_to_domain_entity(model)