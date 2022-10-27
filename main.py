from datetime import datetime

from aiohttp import web
from aiohttp.web_request import Request
from pydantic import BaseModel, ValidationError
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import psycopg2
from sqlalchemy.ext.asyncio import create_async_engine
from config import settings
import aiohttp_jinja2
import jinja2

from handlers import hello, user, create_user, graph, users, table, update_user_form, edit_user
from init_db import init_db
from src.user.db import get_all_users
from src.user.domain import User

if __name__ == '__main__':
    app = web.Application()
    app['engine'] = create_async_engine(settings.data_base_url)
    init_db()
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('./templates'))
    app.add_routes(
        [
            web.get('/hello', hello),
            web.post('/user', user),
            web.post('/edit_user/{user_id}', edit_user),
            web.get('/create_user', create_user),
            web.get('/update_user_form/{user_id}', update_user_form),
            web.get('/graph', graph),
            web.get('/users', users),
            web.get('/table', table),
            web.static('/prefix', './static', show_index=True)
        ]
    )
    web.run_app(app)
