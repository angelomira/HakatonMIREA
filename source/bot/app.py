from aiogram import Dispatcher, types
from loguru import logger

from config import bot_name
from database.create_tables import create_tables
from handlers.general.authentication import cmd_auth
from handlers.general.start_handler import cmd_start
from handlers.general.message_handler import message_handler_fun


async def on_startup(dp: Dispatcher):
    try:
        await create_tables()
        await register_handlers(dp)
        logger.success(f'\n\nSUCCES {bot_name} launched successfully.\n')
    except Exception as err:
        logger.error(f'{err}')


async def on_shutdown():
    logger.success(f'\n\nSUCCES {bot_name} finished successfully.\n')


def trigger(*words):
    def func(message: types.Message):
        return message.text.lower() in words

    return func


@logger.catch()
async def register_handlers(dp: Dispatcher):
    # Main commands
    dp.register_message_handler(cmd_start, commands=['start'])
    dp.register_message_handler(cmd_auth, commands=['auth'])
    dp.register_message_handler(message_handler_fun)
