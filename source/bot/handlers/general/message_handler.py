import re
import time

from aiogram import types
from loguru import logger

from config import waiting_time, session_expiration_time
from database.connect import cursor_users, db_users
from utils.antiflood import rate_limit
import messages as msg
import hashlib
import datetime
import pytz

ANTIFLOOD_TIME = 1


def is_valid_code(code):
    pattern = r'^\d{6}$'
    if re.match(pattern, code):
        return True
    else:
        return False


@logger.catch()
@rate_limit(waiting_time, 'msg')
async def message_handler_fun(message: types.Message):
    user_id = message.from_user.id
    user_msg = message.text

    cursor_users.execute('SELECT user_id FROM logged WHERE user_id = %s AND logged_in = %s', (user_id, True))
    if cursor_users.fetchone() is None:
        cursor_users.execute('SELECT user_id FROM auth WHERE user_id = %s', (user_id,))
        if cursor_users.fetchone() is not None:

            code = is_valid_code(user_msg)
            if code:
                code_hash = hashlib.sha256(user_msg.encode()).hexdigest()
                current_time = time.time()

                cursor_users.execute('SELECT email, expiration FROM auth WHERE user_id = %s AND code_hash = %s', (user_id, code_hash))
                user_info = cursor_users.fetchall()
                if len(user_info) != 0:
                    user_email = user_info[0][0]
                    expiration_time = user_info[0][1]
                    role = 'admin'

                    if current_time < expiration_time:
                        try:
                            cursor_users.execute('INSERT INTO logged VALUES(%s, %s, %s, %s, %s) ON CONFLICT(user_id) '
                                                 'DO UPDATE SET email = %s, role = %s, logged_in = %s, expiration = %s',
                                                 (user_id, user_email, role, True, current_time + session_expiration_time, user_email,
                                                  role, True, current_time + session_expiration_time))
                            cursor_users.execute('DELETE FROM auth WHERE user_id = %s', (user_id,))
                            db_users.commit()

                            current_date = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
                            current_date = current_date.timestamp()
                            logging_time = datetime.datetime.fromtimestamp(current_date).strftime('%d-%m-%Y в %H:%M:%S')

                            await message.answer(text=msg.auth_logging_success_msg.format(user_email=user_email,
                                                                                          logging_time=logging_time))
                        except Exception as err:
                            logger.error(err)
                            db_users.rollback()
                            await message.answer(text=msg.unknown_error_msg)
                            return

                    else:
                        try:
                            cursor_users.execute('DELETE FROM auth WHERE user_id = %s AND code_hash = %s', (user_id, code_hash))
                            db_users.commit()
                            await message.answer(text=msg.auth_code_expired_msg)
                        except Exception as err:
                            logger.critical(err)
                            return
                else:
                    try:
                        await message.answer(text=msg.auth_wrong_code_msg)
                        return
                    except Exception as err:
                        logger.critical(err)
                        return
            return

        try:
            await message.answer(msg.auth_need_msg)
            return
        except Exception as err:
            logger.critical(err)
            return

