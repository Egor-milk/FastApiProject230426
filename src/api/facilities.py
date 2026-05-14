
from fastapi import APIRouter, Body
from fastapi.openapi.models import Example
from fastapi_cache.decorator import cache
from src.tasks.tasks import test_task

from src.api.dependencies import DBDep
from src.schemas.facilities import *


router = APIRouter(prefix='/facilities', tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    print("query to db")
    return await db.facilities.get_all()

@router.post("")
async def create_facilities(
        db: DBDep,
        facilities_data: FacilityAdd = Body(openapi_examples={
            '1': Example(
                summary='test1',
                value={
                    'title': 'test1',
                }
            ),
            '2': Example(
                summary='test1',
                value={
                    'title': 'test1',
                }
            ),
        })
):
    data = await db.facilities.add(facilities_data)
    await db.commit()

    #test_task.delay()

    return {"status": "ok", "data": data}

