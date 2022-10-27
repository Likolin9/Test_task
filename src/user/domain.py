from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    fio: str
    job_title: str
    celery: str
    invite_date: str
    boss_id: str


class UpdateUserRequest(User):
    user_id: str
