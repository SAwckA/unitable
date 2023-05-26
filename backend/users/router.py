from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi_utils.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from .schema import *
from database.psql import get_db

from .usecase import UserUsecase, LoginFailed

from database.cache import redis_pool
from service.auth import UserAuth


router = APIRouter()


@cbv(router)
class UserRouter:
    usecase: UserUsecase = Depends(UserUsecase(get_db, redis_pool()))

    @router.post('/register')
    async def register_user(self, user: UserCreate) -> str:
        try:
            await self.usecase.create_user(user)
        except:
            raise HTTPException(status_code=409, detail='User already exists')
        return 'OK'

    @router.post('/login')
    async def login_user(self, response: Response, form: LoginForm):
        try:
            user, token = await self.usecase.login(form.username, form.password)
        except LoginFailed as e:
            raise HTTPException(status_code=401, detail=e.msg)

        response.set_cookie('sid', token)
        return user

    @router.post('/logout')
    async def logout(self, request: Request, response: Response, _=Depends(UserAuth(redis_pool()))):
        await self.usecase.logout(request.cookies.get('sid'))
        response.set_cookie('sid', max_age=0)
        return 'OK'
