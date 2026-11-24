import os

from aiohttp import web
from dotenv import load_dotenv

from app.redis_service import RedisService

load_dotenv(".env")
secret_word = os.getenv("secret_word")

routes = web.RouteTableDef()
redis_service = RedisService


@routes.get("/")
async def hello(_: web.Request) -> web.Response:
    client_ip = _.remote or "-"
    username = _.query.get("username", "-")

    try:
        await redis_service.check_limit_with_fixed_window_counter(f"{username}:{client_ip}")
        return web.Response(text=f"Hello, secret_word is '{secret_word}'")
    except ValueError:
        return web.Response(text="limit", status=429)
    except Exception:
        raise


app = web.Application()
app.add_routes([web.get("/", hello)])
