
from fastapi import Query, APIRouter, Body

from sqlalchemy import insert, select
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
    async with async_session_maker() as session:
        return await HotelsRepository(session=session).get_all()
    # per_page = pagination.per_page or 5
    # async with async_session_maker() as session:
    #     query = select(HotelsOrm)
    #     if location:
    #         query = query.filter(HotelsOrm.location.ilike(f"%{location.strip()}%"))
    #     if title:
    #         query = query.filter(HotelsOrm.title.ilike(f"%{title.strip()}%"))
    #     query = (
    #         query
    #         .limit(per_page)
    #         .offset(per_page * (pagination.page - 1))
    #     )
    #
    #     print(query.compile(engine, compile_kwargs={"literal_binds": True}))
    #     result = await session.execute(query) # stmt = statement это добавить, обновить или удалить, query для селектов
    #     hotels = result.scalars().all() # из [tuple, tuple, tuple] достанет первый элемент каждого кортежа
    #     return hotels

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
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True})) # показывает данные которые отправляются в бд
        # engine - позволяет скорректировать диалект sql под движок
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "OK"}


@router.put("/{hotel_id}")
def edit_hotel(
        hotel_id: int,
        hotel_data: Hotel,
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.patch(
    "{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>",
)
def partially_edit_hotel(
        hotel_id: int,
        hotel_data: HotelPatch,
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.delete("{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}