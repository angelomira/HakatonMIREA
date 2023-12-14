from config import host_psql, user_psql, password_psql, db_name_psql, port_psql
import datetime
import psycopg2
from loguru import logger

dtime = datetime.datetime.now().strftime("%H:%M:%S")
logger.debug(f'Database start connecting...')

try:
    db_users = psycopg2.connect(
        host=host_psql,
        user=user_psql,
        password=password_psql,
        database=db_name_psql,
        port=port_psql,
        )

    cursor_users = db_users.cursor()

    logger.success(f'Database succesfully connected!')

except psycopg2.Error as err:
    logger.error(f'{err}')

