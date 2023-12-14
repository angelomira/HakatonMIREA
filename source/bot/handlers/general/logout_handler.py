from aiogram import types
from loguru import logger

import messages as msg
from config import (
    waiting_time
)
from database.connect import cursor_users, db_users
from utils.antiflood import rate_limit


@logger.catch()
@rate_limit(waiting_time, 'logout')
async def cmd_logout(message: types.Message):
    user_id = message.from_user.id

    try:
        cursor_users.execute('UPDATE logged SET logged_in = %s WHERE user_id = %s', (False, user_id))
        db_users.commit()
        await message.answer(text=msg.auth_session_logout_msg)
    except Exception as err:
        logger.error(f'{err}')
        return
