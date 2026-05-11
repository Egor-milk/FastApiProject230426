from datetime import date
import json
from fastapi import Query, APIRouter, Body, HTTPException

from sqlalchemy.exc import MultipleResultsFound

from src.api.dependencies import PaginationDep, DBDep
from src.init import redis_manager
from src.schemas.facilities import *


router = APIRouter(prefix='/facilities', tags=["Удобства"])


@router.get("")
async def get_facilities(
        db: DBDep,
):
    facilities_from_cache = await redis_manager.get("facilities")
    print(f"{facilities_from_cache}")
    if not facilities_from_cache:
        print("query to db")
        facilities = await db.facilities.get_all()
        facilities_schemas: list[dict] = [f.model_dump() for f in facilities]
        facilities_json = json.dumps(facilities_schemas)
        await redis_manager.set("facilities", facilities_json, expire=10)

        return facilities
    else:
        facilities_dict = json.loads(facilities_from_cache)
        return facilities_dict
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

