from datetime import date

from fastapi import Query, APIRouter, Body, HTTPException

from sqlalchemy.exc import MultipleResultsFound

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.facilities import *


router = APIRouter(prefix='/facilities', tags=["Удобства"])


@router.get("")
async def get_facilities(
        db: DBDep,
):
    return await db.facilities.get_all()

@router.post("")
async def create_facilities(
        db: DBDep,
        facilities_data: FacilityAdd = Body(openapi_examples={
                '1': {
                    'summary': 'test1',
                    'value': {
                        'title': 'test1',
                      }
                },
                '2': {
                    'summary': 'test2',
                    'value': {
                        'title': 'test2'
                      }
                }
            })
):
    data = await db.facilities.add(facilities_data)
    await db.commit()
    return {"status": "ok", "data": data}

