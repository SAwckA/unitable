from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    psql_conn_string: str = Field(..., env='PG_CONN_STRING')
    secret_key: str = Field(..., env='SECRET_KEY')
    debug: bool = Field(..., env='DEBUG')

    class Config:
        env_file = '.env'
