from typing import Optional

from sqlmodel import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from .schema import User, UserCreate
from redis.asyncio import Redis
from argon2 import PasswordHasher

from uuid import uuid4


class LoginFailed(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return f'<LoginFailed cause: {self.msg}>'


class UserUsecase:
    session: AsyncSession
    cache: Redis

    def __init__(self, session, cache: Redis):
        self.session_gen = session
        self.cache = cache

    async def __call__(self):
        self.session = await anext(self.session_gen())
        return self

    async def create_user(self, new_user: UserCreate) -> User:
        user = User.from_orm(new_user)
        user.password = PasswordHasher().hash(new_user.password)
        self.session.add(user)
        await self.session.commit()
        return user

    async def _check_user(self, username: str, password: str) -> Optional[User]:
        res = await self.session.execute(select(User).where(or_(User.username == username,User.email == username)))
        user = res.one_or_none()
        if user is None:
            return None
        user = user[0]
        if PasswordHasher().verify(user.password, password):
            return user
        return None

    async def login(self, username: str, password: str) -> tuple[User, str]:
        """(User, token)"""
        res = await self._check_user(username, password)
        if res is None:
            raise LoginFailed('invalid credentials')
        token = uuid4().__str__()
        await self.cache.set(token, res.json())
        return res, token

    async def logout(self, token: str):
        await self.cache.delete(token)