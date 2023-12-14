#!python
# -*- coding : utf-8 -*-

import aiogram.utils.exceptions
import sys
import os


def main():
    # import sys, os
    # sys.path.append(os.getcwd())

    from loader import dp
    from loguru import logger
    from aiogram import executor
    from app import on_startup, on_shutdown
    from utils.antiflood import ThrottlingMiddleware

    logger.add("logs/debug.log", format='{time} {level} {message}', colorize=True, rotation="00:00", compression='zip', diagnose=False)
    # logger.add("logs_clicks/debug_clicks.log", filter=lambda record: record["extra"]["task"] == "A", format='{time} {level} {message}', colorize=True, rotation="00:00", compression='zip', diagnose=False)

    dp.middleware.setup(ThrottlingMiddleware())

    try:
        executor.start_polling(dp, on_startup=on_startup, skip_updates=True, relax=None, timeout=10, fast=True)
    except aiogram.utils.exceptions.NetworkError as err:
        logger.critical(f'{err}')
        python = sys.executable
        os.execl(python, python, *sys.argv)


if __name__ == '__main__':
    main()
