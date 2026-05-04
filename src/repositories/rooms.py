from pydantic import BaseModel
from sqlalchemy import select

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    # async def get_all(self, hotel_id, *args, **kwargs):
    #     query = select(self.model).filter_by(hotel_id=hotel_id)
    #     result = await self.session.execute(query)
    #     return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
