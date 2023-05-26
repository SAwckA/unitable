from redis.asyncio import Redis
from fastapi import Request, Cookie, HTTPException
from users.schema import User

class UserAuth:

    def __init__(self, cache: Redis):
        self.cache = cache

    async def __call__(self, session_token: str | None = Cookie(default=None, alias='sid')) -> User:
        if session_token is None:
            raise HTTPException(status_code=401, detail='No cookie found')
        user = await self.cache.get(session_token)
        if user is None:
            raise HTTPException(status_code=401, detail='Invalid token')
        user_model = User.parse_raw(user, encoding='utf-8')
        return user_model

