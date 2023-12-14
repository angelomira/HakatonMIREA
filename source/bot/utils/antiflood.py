import time

from aiogram import Dispatcher, types
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled

from config import black_list
from database.connect import cursor_users, db_users
import messages as msg
from loguru import logger


# Antiflood
def rate_limit(limit: int, key=None):
    """
    Decorator for configuring rate limit and key in different functions.
    :param limit:
    :param key:
    :return:
    """

    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)

        return func

    return decorator


async def message_throttled(message: types.Message):

    pass


class ThrottlingMiddleware(BaseMiddleware):
    """
    Simple middleware
    """

    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):

        """
        This handler is called when dispatcher receives a message
        :param data:
        :param message:
        """

        # Get current handler
        # if message.from_user.id not in admin_id_list:
        #     print(f'{message.from_user.id} не смог.')
        #     raise CancelHandler()

        user_id = message.from_user.id

        if user_id in black_list:
            print(f'{user_id} banned')

        cursor_users.execute('SELECT expiration, logged_in FROM logged WHERE user_id = %s', (user_id,))
        user_info = cursor_users.fetchone()
        if user_info is not None:
            expiration_time = user_info[0]
            logged_in = user_info[1]
            current_time = time.time()

            if (current_time > expiration_time) and logged_in:
                try:
                    cursor_users.execute('UPDATE logged SET logged_in = %s WHERE user_id = %s', (False, user_id))
                    db_users.commit()
                    await message.answer(text=msg.auth_session_expired_msg)
                except Exception as err:
                    logger.error(f'{err}')
                    return
                finally:
                    raise CancelHandler()

        else:
            await message.answer(text=msg.auth_need_msg)
            raise CancelHandler()

        handler = current_handler.get()

        # Get dispatcher from context
        dispatcher = Dispatcher.get_current()
        # If handler was configured, get rate limit and key from handler
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"

        # Use Dispatcher.throttle method.
        try:
            await dispatcher.throttle(key, rate=limit)

        except Throttled:
            # Execute action
            await message_throttled(message)
            # Cancel current handler
            raise CancelHandler()
