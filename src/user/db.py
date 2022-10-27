from src.user.domain import User, UpdateUserRequest
from datetime import datetime

from aiohttp import web
from aiohttp.web_request import Request
from pydantic import BaseModel, ValidationError
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, update, select
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import psycopg2
from sqlalchemy.ext.asyncio import create_async_engine
import aiohttp_jinja2
import jinja2


meta = MetaData()


users_table = Table(
    'users', meta,
    Column('id', Integer, primary_key=True),
    Column('fio', String),
    Column('job_title', String),
    Column('celery', String),
    Column('invite_date', String),
    Column('boss_id', Integer),
)


async def get_all_users(app):
    async with app['engine'].begin() as conn:
        result = await conn.execute(
            users_table.select()
        )
        return [user for user in result]


async def get_user(app, user_id: int):
    async with app['engine'].begin() as conn:
        return (await conn.execute(
            select(users_table).where(users_table.c.id == int(user_id))
        )).first()


async def save_user(app, user: User):
    async with app['engine'].begin() as conn:
        await conn.execute(
            users_table.insert().values(
                job_title=user.job_title,
                fio=user.fio,
                celery=user.celery,
                invite_date=user.invite_date,
                boss_id=int(user.boss_id) if user.boss_id else None
            )
        )


async def update_user(app, user: UpdateUserRequest):
    async with app['engine'].begin() as conn:
        await conn.execute(
            update(users_table).
            where(users_table.c.id == int(user.user_id)).
            values(
                job_title=user.job_title,
                fio=user.fio,
                celery=user.celery,
                invite_date=user.invite_date,
                boss_id=int(user.boss_id) if user.boss_id else None
            )
        )
