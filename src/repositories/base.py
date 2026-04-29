from sqlalchemy import select


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        #print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)  # stmt = statement это добавить, обновить или удалить, query для селектов
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        #print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)  # stmt = statement это добавить, обновить или удалить, query для селектов
        return result.scalars().one_or_none()