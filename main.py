import uvicorn
from fastapi import FastAPI
from fastapi import Query, Body

app = FastAPI()

hotels = [
    {'id': 1, 'title': 'Sochi'},
    {'id': 2, 'title': 'Dubai'},
]


@app.get("/hotels")
def get_hotels(
        id: int | None = Query(None, description='Айдишник'),
        title: str | None = Query(None, description='Название отеля'),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)
    return hotels_

@app.post("/hotels")
def create_hotel(
        title: str = Body(embed=True), #embed = бэк будет ожидать json а не просто строку
):
    global hotels
    hotels.append({'id': hotels[-1]['id'] + 1, 'title': title})

@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'ok'}

@app.put('/hotels/{hotel_id}')
def put_hotel(
    hotel_id: int,
    new_hotel_id : int = Body(embed=True),
    new_title: str = Body(embed=True),
):
    global hotels
    hotels_ = []
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['id'] = new_hotel_id
            hotel['title'] = new_title
        hotels_.append(hotel)
    hotels = hotels_
    return {'status': 'ok'}

@app.patch('/hotels/{hotel_id}')
def patch_hotel(
    hotel_id: int,
    new_hotel_id : int | None = Body(embed=True),
    new_title: str | None = Body(embed=True),
):
    global hotels
    hotels_ = []
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            if new_hotel_id:
                hotel['id'] = new_hotel_id
            if new_title:
                hotel['title'] = new_title
        hotels_.append(hotel)
    hotels = hotels_
    return {'status': 'ok'}

if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)