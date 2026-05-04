
from fastapi import Query, APIRouter, Body, HTTPException

from sqlalchemy import insert, select
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.repositories.rooms import RoomsRepository
from src.schemas.hotels import Hotel, HotelPatch, HotelAdd
from src.schemas.rooms import RoomAdd, RoomAddRequest

router = APIRouter(prefix='/hotels', tags=["Комнаты"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        hotel_id: int,
):
    async with async_session_maker() as session:
        return await RoomsRepository(session=session).get_all(hotel_id)

# @router.get("/{hotel_id}")
# async def get_hotel(hotel_id: int):
#     async with async_session_maker() as session:
#         try:
#             return await HotelsRepository(session=session).get_one_or_none(id=hotel_id)
#         except MultipleResultsFound:
#             raise HTTPException(status_code=400, detail='multiple result found')
#
#
#
@router.post("/{hotel_id}/rooms")
async def create_rooms(
        hotel_id: int,
        rooms_data: RoomAddRequest = Body(
            openapi_examples={
                "1": {
                    "summary": "test_room_1",
                    "value": {
                        "title": "luxe_1",
                        "description": "very luxe room",
                        "price": 10000,
                        "quantity": 1,
                    }
                },
                "2": {
                    "summary": "test_room_2",
                    "value": {
                        "title": "econom",
                        "description": "low price room",
                        "price": 100,
                        "quantity": 10,
                    }
                }
            })
):
    _rooms_data = RoomAdd(hotel_id=hotel_id, **rooms_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session=session).add(data=_rooms_data)
        await session.commit()

    return {"status": "OK", "data": room}

#
# @router.put("/{hotel_id}")
# async def edit_hotel(
#         hotel_id: int,
#         hotel_data: HotelAdd,
# ):
#     async with async_session_maker() as session:
#         try:
#             result = await HotelsRepository(session=session).edit(data=hotel_data, id=hotel_id)
#             await session.commit()
#             return {"status": "OK", "data": result}
#         except NoResultFound:
#             await session.rollback()
#             raise HTTPException(status_code=404, detail='no result found')
#         except MultipleResultsFound:
#             await session.rollback()
#             raise HTTPException(status_code=400, detail='multiple result found')
#
#
# @router.patch(
#     "{hotel_id}",
#     summary="Частичное обновление данных об отеле",
#     description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>",
# )
# async def partially_edit_hotel(
#         hotel_id: int,
#         hotel_data: HotelPatch,
# ):
#     async with async_session_maker() as session:
#         try:
#             result = await HotelsRepository(session=session).edit(exclude_unset=True, data=hotel_data, id=hotel_id)
#             await session.commit()
#             return {"status": "OK", "data": result}
#         except NoResultFound:
#             await session.rollback()
#             raise HTTPException(status_code=404, detail='no result found')
#         except MultipleResultsFound:
#             await session.rollback()
#             raise HTTPException(status_code=400, detail='multiple result found')
#
#
# @router.delete("{hotel_id}")
# async def delete_hotel(hotel_id: int):
#     async with async_session_maker() as session:
#         try:
#             result = await HotelsRepository(session=session).delete(id=hotel_id)
#             await session.commit()
#             return {"status": "OK", "data": result}
#         except NoResultFound:
#             await session.rollback()
#             raise HTTPException(status_code=404, detail='no result found')
#         except MultipleResultsFound:
#             await session.rollback()
#             raise HTTPException(status_code=400, detail='multiple result found')