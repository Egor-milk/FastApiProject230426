from datetime import date

from fastapi import Query, APIRouter, Body, HTTPException

from sqlalchemy.exc import MultipleResultsFound

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import Hotel, HotelPatch, HotelAdd


router = APIRouter(prefix='/hotels', tags=["Отели"])


@router.get("")
async def get_hotels( #теперь выдает только отели где есть свободные номера
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Местоположение"),
        date_from: date = Query(example="2026-01-01"),
        date_to: date = Query(example="2026-02-01"),
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_filtered_by_time(
         location=location,
         title=title,
         date_from=date_from,
         date_to=date_to,
         limit=per_page,
         offset=per_page * (pagination.page - 1)
    )

@router.get("/{hotel_id}")
async def get_hotel(
        db: DBDep,
        hotel_id: int,
):
    try:
        return await db.hotels.get_one_or_none(id=hotel_id)
    except MultipleResultsFound:
        raise HTTPException(status_code=400, detail='multiple result found')



@router.post("")
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd = Body(
            openapi_examples={
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
    hotel = await db.hotels.add(data=hotel_data)
    await db.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def edit_hotel(
        db: DBDep,
        hotel_id: int,
        hotel_data: HotelAdd,
):
    result = await db.hotels.edit(data=hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK", "data": result}


@router.patch(
    "{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>",
)
async def partially_edit_hotel(
        db: DBDep,
        hotel_id: int,
        hotel_data: HotelPatch,
):
    result = await db.hotels.edit(exclude_unset=True, data=hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK", "data": result}


@router.delete("{hotel_id}")
async def delete_hotel(
        db: DBDep,
        hotel_id: int
):
    result = await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK", "data": result}