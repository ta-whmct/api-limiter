from aiohttp import web

from app.redis_service import RedisService

routes = web.RouteTableDef()
redis_service = RedisService


@routes.get("/")
async def hello(_: web.Request) -> web.Response:
    client_ip = _.remote or "-"
    try:
        await redis_service.check_limit_with_fixed_window_counter(client_ip)
        return web.Response(text="Hello, world")
    except ValueError:
        return web.Response(text="limit", status=429)
    except Exception:
        raise


app = web.Application()
app.add_routes([web.get("/", hello)])
