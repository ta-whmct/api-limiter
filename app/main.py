from aiohttp import web

routes = web.RouteTableDef()


@routes.get("/")
async def hello(_: web.Request) -> web.Response:
    return web.Response(text="Hello, world")


app = web.Application()
app.add_routes([web.get("/", hello)])
