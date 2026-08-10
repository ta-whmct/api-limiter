from aiohttp import web

from app.main import app

if __name__ == "__main__":
    web.run_app(app, host="127.0.0.1", port=8000)
