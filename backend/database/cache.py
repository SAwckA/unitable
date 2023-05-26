from redis.asyncio import Redis, from_url
from config.settings import Settings

redis_instance = None


def redis_pool() -> Redis:
    global redis_instance
    if redis_instance is None:
        print('Init')
        instance = from_url(f'redis://{Settings().redis_host}:{Settings().redis_port}',
                            password=Settings().redis_password,
                            encoding='utf-8',
                            decode_responses=True)
        redis_instance = instance
        return instance
    return redis_instance

