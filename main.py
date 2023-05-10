from fastapi import FastAPI
# from database import sqlite
from database import psql
from journal.router import router as journal_router


app = FastAPI()


@app.on_event('startup')
async def database_init():
    await psql.init_db()


app.include_router(journal_router)
