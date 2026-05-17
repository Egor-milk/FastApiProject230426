from src.schemas.facilities import FacilityAdd
from src.services.base import BaseService
from src.tasks.tasks import test_task



class FacilityService(BaseService):
    async def create_facilities(self, facilities_data: FacilityAdd):
        facility = await self.db.facilities.add(facilities_data)
        await self.db.commit()

        test_task.delay()
        return facility
