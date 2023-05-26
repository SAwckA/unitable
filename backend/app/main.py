from fastapi import FastAPI
# from database import sqlite
from database import psql
from journal.router import router as journal_router
from users.router import router as user_router
from database.cache import redis_pool


app = FastAPI()
redis_instance = None


@app.on_event('startup')
async def postgres_database_init():
    await psql.init_db()
    global redis_instance
    redis_instance = redis_pool()


app.include_router(journal_router)
app.include_router(user_router)
