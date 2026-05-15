async def test_get_facilities(ac):
    response = await ac.get("/facilities")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_post_facilities(ac):
    facility_title = "test1dsada"
    response = await ac.post("/facilities", json={"title": facility_title})
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json().get("data").get("title") == facility_title
    assert "data" in response.json()
