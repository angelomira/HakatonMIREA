from aiogram import types
from loguru import logger

import messages as msg
from config import waiting_time
from utils.antiflood import rate_limit


@logger.catch()
@rate_limit(waiting_time, 'start')
async def cmd_start(message: types.Message):
    try:
        first_name = message.from_user.first_name
        user_id = message.from_user.id

        await message.answer(msg.auth_start_msg.format(first_name=first_name))
        logger.debug(f'{user_id} Использовал /start')

    except Exception as err:
        logger.error(err)
        return
