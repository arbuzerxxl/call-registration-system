from pony.orm import Database, Required

db_user_appeal = Database()

DB_CONFIG = dict(
    provider='postgres',
    user='postgres',
    password='password',
    database='user_appeal',
    host='db',
    port=5432)

db_user_appeal.bind(**DB_CONFIG)


class UserAppeal(db_user_appeal.Entity):
    first_name = Required(str)
    last_name = Required(str)
    patronymic = Required(str)
    phone_number = Required(int, size=64, unique=True, sql_type='BIGINT')
    appeal = Required(str)
