import os
from pony.orm import Database, Required

POSTGRES_USER_appeal = Database()

DB_CONFIG = dict(
    provider=os.environ.get('DB_PROVIDER', 'postgres'),
    user=os.environ.get('POSTGRES_USER', 'postgres'),
    password=os.environ.get('POSTGRES_PASSWORD', 'password'),
    database=os.environ.get('POSTGRES_DB', 'user_appeal'),
    host=os.environ.get('DB_HOST', 'localhost'),
    port=os.environ.get('DB_PORT', '5433'))

POSTGRES_USER_appeal.bind(**DB_CONFIG)


class UserAppeal(POSTGRES_USER_appeal.Entity):
    first_name = Required(str)
    last_name = Required(str)
    patronymic = Required(str)
    phone_number = Required(int, size=64, sql_type='BIGINT')
    appeal = Required(str)
