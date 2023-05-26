from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    psql_conn_string: str = Field(..., env='PG_CONN_STRING')
    secret_key: str = Field(..., env='SECRET_KEY')
    debug: bool = Field(..., env='DEBUG')

    redis_password: str = Field(..., env='REDIS_PASS')
    redis_host: str = Field(..., env='REDIS_HOST')
    redis_port: str = Field(..., env='REDIS_PORT')

    class Config:
        env_file = '.env'
