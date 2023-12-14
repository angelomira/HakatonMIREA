import time

from aiogram import types
from loguru import logger

import messages as msg
from config import (
    waiting_time,
    email_login,
    email_pass,
    send_code_delay,
    code_expiration_time,
    max_attempts_code
)
from database.connect import cursor_users, db_users
from loader import bot
from modules.num_formating import numerize
from utils.antiflood import rate_limit
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils.encrypter import generate_and_encrypt_code
import time


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

