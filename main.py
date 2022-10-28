
from aiohttp import web
from sqlalchemy.ext.asyncio import create_async_engine
from config import settings
import aiohttp_jinja2
import jinja2

from handlers import user, create_user, users, table, update_user_form, edit_user
from init_db import init_db

if __name__ == '__main__':
    app = web.Application()
    app['engine'] = create_async_engine(settings.data_base_url)
    init_db()
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('./templates'))
    app.add_routes(
        [
            web.post('/user', user),
            web.post('/edit_user/{user_id}', edit_user),
            web.get('/create_user', create_user),
            web.get('/update_user_form/{user_id}', update_user_form),
            web.get('/users', users),
            web.get('/table', table)
        ]
    )
    web.run_app(app)
