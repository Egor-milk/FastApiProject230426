
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
import uvicorn



sys.path.append(str(Path(__file__).parent.parent)) #костыль, скорее всего потом удалится.
# Нужен чтобы работал следующий имп
from src.init import redis_manager
from src.api.hotels import router as router_hotels
from src.api.auth import router as router_auth
from src.api.rooms import router as router_rooms
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities

@asynccontextmanager
async def lifespan(app: FastAPI):
    # при старте приложения
    await redis_manager.connect()
    yield
    await redis_manager.close()
    # при выключении или перезагрузке

app = FastAPI(lifespan=lifespan)

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
