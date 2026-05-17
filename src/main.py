import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
import uvicorn
import logging

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend


sys.path.append(str(Path(__file__).parent.parent))  # костыль, скорее всего потом удалится.

logging.basicConfig(level=logging.DEBUG)

from src.init import redis_manager # noqa
from src.api.hotels import router as router_hotels # noqa
from src.api.auth import router as router_auth # noqa
from src.api.rooms import router as router_rooms # noqa
from src.api.bookings import router as router_bookings # noqa
from src.api.facilities import router as router_facilities # noqa
from src.api.images import router as router_images # noqa


@asynccontextmanager
async def lifespan(app: FastAPI):
    # при старте приложения
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi_cache")
    logging.info("FastAPICache initialized")
    yield
    await redis_manager.close()
    # при выключении или перезагрузке


app = FastAPI(lifespan=lifespan)

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)
app.include_router(router_images)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
