from sqlalchemy import create_engine
from config import settings

from src.user.db import meta

INIT_SQL = """INSERT INTO public.users (id, fio, job_title, celery, invite_date, boss_id) VALUES (1, 'Boss Bossovich Bosenko', 'Head of Head', '17000', '2019-05-08', NULL);
INSERT INTO public.users (id, fio, job_title, celery, invite_date, boss_id) VALUES (2, 'Chernenko Vsevolod', 'Python developer', '1300', '2022-11-01', 1);
INSERT INTO public.users (id, fio, job_title, celery, invite_date, boss_id) VALUES (3, 'Andrienko Andrei Andreevich', 'python dev', '1100', '2022-10-11', 1);
INSERT INTO public.users (id, fio, job_title, celery, invite_date, boss_id) VALUES (4, 'Ivanenko Ivan Ivanovich', 'Python developer', '900', '2022-10-12', 1);
SELECT pg_catalog.setval('public.users_id_seq', 4, true);
"""


def init_db():
    engine = create_engine(settings.data_base_url_sync)
    meta.create_all(engine)
    try:
        engine.execute(INIT_SQL)
    except:
        pass