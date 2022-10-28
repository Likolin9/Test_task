from aiohttp import web
from aiohttp.web_request import Request
from pydantic import ValidationError

import aiohttp_jinja2
from config import settings
from src.user.db import get_all_users, save_user, update_user, get_user
from src.user.domain import User, UpdateUserRequest

BASE_URl = f'http://{settings.domain}:{settings.port}'


async def user(request: Request):
    data = await request.post()
    try:
        await save_user(request.app, User(**data))
    except ValidationError:
        return web.HTTPBadRequest()
    raise web.HTTPFound('/users')


async def edit_user(request: Request):
    data = await request.post()
    try:
        await update_user(request.app, UpdateUserRequest(user_id=request.match_info['user_id'], **data))
    except ValidationError:
        return web.HTTPBadRequest()
    raise web.HTTPFound('/users')


@aiohttp_jinja2.template('users.html')
async def users(request):
    all_users = await get_all_users(request.app)

    return {
        'users': all_users,
        'base_url': BASE_URl

    }


@aiohttp_jinja2.template('create_user.html')
def create_user(request):
    boss_id = request.rel_url.query.get('boss_id')

    return {
        'boss_id': boss_id,

    }


@aiohttp_jinja2.template('update_user.html')
async def update_user_form(request):
    user_ = await get_user(request.app, user_id=request.match_info['user_id'])
    return {
        'boss_id': user_.boss_id,
        'user': user_,
    }


@aiohttp_jinja2.template('table.html')
async def table(request):
    all_users = await get_all_users(request.app)
    return {'users': all_users}
