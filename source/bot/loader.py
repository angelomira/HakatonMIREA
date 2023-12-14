from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from config import token, host_redis, db_redis, port_redis, pool_size_redis

storage = RedisStorage2(host=host_redis, port=port_redis, db=db_redis, pool_size=pool_size_redis)
bot = Bot(token=token, parse_mode='html')
dp = Dispatcher(bot=bot, storage=storage)
