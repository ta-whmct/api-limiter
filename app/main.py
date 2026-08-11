from aiohttp import web

from app.redis_service import RedisService

routes = web.RouteTableDef()
redis_service = RedisService


@routes.get("/fixed-window")
async def fixes_window(_: web.Request) -> web.Response:
    client_ip = _.remote or "-"
    username = _.query.get("username", "-")

    try:
        await redis_service.check_limit_with_fixed_window_counter(f"{username}:{client_ip}")
        return web.Response(text="Hello, world")
    except ValueError:
        return web.Response(text="request limit reached", status=429)
    except Exception:
        raise


app = web.Application()
app.add_routes([web.get("/", fixes_window)])
