from loguru import logger

from database.connect import cursor_users, db_users
from database.tables import (
    table_auth,
    table_logged,
    table_tempblocked,
    table_occupied_rooms,
    table_student_card
)


async def create_tables():
    try:
        cursor_users.execute(table_auth)
        cursor_users.execute(table_logged)
        cursor_users.execute(table_tempblocked)
        cursor_users.execute(table_occupied_rooms)
        cursor_users.execute(table_student_card)

        db_users.commit()

        logger.success('All tables created / loaded.')
    except Exception as err:
        logger.error(f'{err}')
