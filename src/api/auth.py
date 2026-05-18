from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import ObjectAlreadyExistsException, UserAlreadyExistsHTTPException, WrongEmailException, \
    WrongEmailHTTPException, WrongPasswordException, WrongPasswordHTTPException, UserAlreadyExistsException
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

@router.post("/register")
async def register_user(
    db: DBDep,
    data: UserRequestAdd,
):
    try:
        await AuthService(db).register_user(data=data)
    except UserAlreadyExistsException:
        raise UserAlreadyExistsHTTPException
    return {"status": "OK"}


@router.post("/login")
async def login_user(
    db: DBDep,
    data: UserRequestAdd,
    response: Response,
):
    try:
        access_token = await AuthService(db).login_user(data=data)
    except WrongEmailException as ex:
        raise WrongEmailHTTPException from ex
    except WrongPasswordException as ex:
        raise WrongPasswordHTTPException from ex
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}



@router.get("/me")
async def get_me(
    db: DBDep,
    user_id: UserIdDep,
):
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.post("/logout")
async def logout_user(
    response: Response,
):
    response.delete_cookie("access_token")
    return {"status": "OK"}
