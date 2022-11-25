import os
from pony.orm import Database, Required

db_user_appeal = Database()

DB_CONFIG = dict(
    provider=os.environ.get('DB_PROVIDER', 'postgres'),
    user=os.environ.get('DB_USER', 'postgres'),
    password=os.environ.get('DB_PASSWORD', 'password'),
    database=os.environ.get('DB_DATABASE', 'user_appeal'),
    host=os.environ.get('DB_HOST', 'localhost'),
    port=os.environ.get('DB_PORT', '5433'))

db_user_appeal.bind(**DB_CONFIG)


class UserAppeal(db_user_appeal.Entity):
    first_name = Required(str)
    last_name = Required(str)
    patronymic = Required(str)
    phone_number = Required(int, size=64, sql_type='BIGINT')
    appeal = Required(str)
