
from fastapi import Query, APIRouter, Body, HTTPException

from sqlalchemy import insert, select, exc
from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPatch

router = APIRouter(prefix='/hotels')



@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Местоположение")
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session=session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )

@router.post("")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    '1': {
        'summary': 'sochi',
        'value': {
            'title': 'hotel',
            'location': 'sochi',
          }
    },
    '2': {
        'summary': 'dubai',
        'value': {
            'title': 'hotel_2',
            'location': 'dubai',
          }
    }
})
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session=session).add(
            data=hotel_data
        )
        await session.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def edit_hotel(
        hotel_id: int,
        hotel_data: Hotel,
):
    async with async_session_maker() as session:
        try:
            result = await HotelsRepository(session=session).edit(data=hotel_data, id=hotel_id)
            await session.commit()
            return {"status": "OK", "data": result}
        except exc.NoResultFound:
            await session.rollback()
            raise HTTPException(status_code=404, detail='no result found')
        except exc.MultipleResultsFound:
            await session.rollback()
            raise HTTPException(status_code=400, detail='multiple result found')


@router.patch(
    "{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>",
)
async def partially_edit_hotel(
        hotel_id: int,
        hotel_data: HotelPatch,
):
    async with async_session_maker() as session:
        try:
            result = await HotelsRepository(session=session).edit(exclude_unset=True, data=hotel_data, id=hotel_id)
            await session.commit()
            return {"status": "OK", "data": result}
        except exc.NoResultFound:
            await session.rollback()
            raise HTTPException(status_code=404, detail='no result found')
        except exc.MultipleResultsFound:
            await session.rollback()
            raise HTTPException(status_code=400, detail='multiple result found')


@router.delete("{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        try:
            result = await HotelsRepository(session=session).delete(id=hotel_id)
            await session.commit()
            return {"status": "OK", "data": result}
        except exc.NoResultFound:
            await session.rollback()
            raise HTTPException(status_code=404, detail='no result found')
        except exc.MultipleResultsFound:
            await session.rollback()
            raise HTTPException(status_code=400, detail='multiple result found')