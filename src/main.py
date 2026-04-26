import sys
from pathlib import Path

from fastapi import FastAPI
import uvicorn

sys.path.append(str(Path(__file__).parent.parent)) #костыль, скорее всего потом удалится.
# Нужен чтобы работал следующий имп
from src.api.hotels import router as router_hotels
from src.config import settings


print(f'{settings.DB_URL=}')




app = FastAPI()

app.include_router(router_hotels, tags=["hotels"])

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
