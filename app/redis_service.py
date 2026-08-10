import redis.asyncio as redis

REQUEST_LIMIT = 2
LIMIT_WINDOWS_IN_SEC = 20


class RedisService:
    host: str = "localhost"
    port: int = 6379
    user: str = "default"

    @classmethod
    async def get_key(cls, key: str) -> bytes | str | None:
        async with redis.Redis(host=cls.host, port=cls.port, username=cls.user) as conn:
            return await conn.get(key)

    @classmethod
    async def set_key(cls, key: str, value: str) -> None:
        async with redis.Redis(host=cls.host, port=cls.port, username=cls.user) as conn:
            await conn.set(name=key, value=value)

    @classmethod
    async def check_limit_with_fixed_window_counter(cls, key: str) -> None:
        async with redis.Redis(host=cls.host, port=cls.port, username=cls.user) as conn:
            count = await cls.get_key(key)
            if count and int(count) >= REQUEST_LIMIT:
                msg = "request not allowed"
                raise ValueError(msg) from None
            count = await conn.incr(key)
            await conn.expire(key, LIMIT_WINDOWS_IN_SEC)
