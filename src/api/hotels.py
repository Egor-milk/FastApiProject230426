from datetime import date

from fastapi import Query, APIRouter, Body, HTTPException
from fastapi.openapi.models import Example
from fastapi_cache.decorator import cache


from sqlalchemy.exc import MultipleResultsFound

from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import check_date_to_after_date_from, ObjectNotFoundException, HotelNotFoundException
from src.schemas.hotels import HotelPatch, HotelAdd
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=10)
async def get_hotels(  # теперь выдает только отели где есть свободные номера
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Местоположение"),
    date_from: date = Query(default="2026-01-01"),
    date_to: date = Query(default="2026-02-01"),
):
    return await HotelService(db).get_filtered_by_time(
        pagination,
        title,
        location,
        date_from,
        date_to,
    )





@router.get("/{hotel_id}")
async def get_hotel(
    db: DBDep,
    hotel_id: int,
):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except MultipleResultsFound:
        raise HTTPException(status_code=400, detail="multiple result found")
    except ObjectNotFoundException:
        raise HotelNotFoundException


@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": Example(
                summary="sochi",
                value={
                    "title": "hotel",
                    "location": "sochi",
                },
            ),
            "2": Example(
                summary="dubai",
                value={
                    "title": "hotel_2",
                    "location": "dubai",
                },
            ),
        }
    ),
):
    hotel = await HotelService(db).add_hotel(data=hotel_data)
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def edit_hotel(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelAdd,
):
    hotel = HotelService(db).edit_hotel(hotel_id=hotel_id, data=hotel_data)
    return {"status": "OK", "data": hotel}


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
    hotel = HotelService(db).edit_hotel(exclude_unset=True, hotel_id=hotel_id, data=hotel_data)
    return {"status": "OK", "data": hotel}


@router.delete("{hotel_id}")
async def delete_hotel(db: DBDep, hotel_id: int):
    result = await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK", "data": result}
