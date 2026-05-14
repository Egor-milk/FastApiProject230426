import pytest

@pytest.fixture()
async def register_user(email, password, ac, setup_database):
    response = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        }
    )
    return response

@pytest.fixture()
async def authenticated_ac(email, password, register_user, ac):
    await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        }
    )
    yield ac


@pytest.mark.parametrize("email, password", [
    ("test1123123213@mail.ru", "1234asdasd"),
    ("testasfgasdasdqd@mail.ru", "1234asdasdADadasdasd"),
    ("popopopoppopopop@mail.com", "roroworowroworASDaSDasdAS"),
])
async def test_all(email, password, register_user, authenticated_ac, ac):

    assert register_user.status_code == 200

    me = await ac.get("/auth/me")

    assert me.json()["email"] == email
    assert "password" not in me.json()

    await ac.post("/auth/logout")

    me = await ac.get("/auth/me")

    assert me.status_code == 401

#pytest tests/integration_tests/auth/test_api.py -s -v