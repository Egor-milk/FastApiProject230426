from fastapi import FastAPI, Query, Body
import uvicorn
import threading

from hotels import router as router_hotels
app = FastAPI()

app.include_router(router_hotels, tags=["hotels"])

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
