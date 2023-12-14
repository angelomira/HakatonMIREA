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


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@edu\.mirea\.ru$'
    if re.match(pattern, email):
        return True
    else:
        return False


def send_code_to_email(receiver_email, email_code, encrypted_code, user_id):
    try:
        message = MIMEMultipart()
        message["From"] = email_login
        message["To"] = receiver_email
        message["Subject"] = "Подтверите Ваш вход в аккаунт"

        body = f"Ваш код подтверждения: {email_code}\n\n" \
               f"Если Вы не запрашивали код, проигнорируйте данное сообщение.\n\n\n" \
               f"MIREA DORMITORY BOT"
        message.attach(MIMEText(body, "plain"))
    except Exception as err:
        logger.error(f'{err}')
        return

    try:

        smtp_server = smtplib.SMTP_SSL("smtp.mail.ru", 465)
        smtp_server.login(email_login, email_pass)
        smtp_server.sendmail(email_login, receiver_email, message.as_string())
        smtp_server.quit()
        print("Email sent successfully")

    except Exception as e:
        cursor_users.execute('DELETE FROM auth WHERE user_id = %s AND code_hash = %s', (user_id, encrypted_code))
        db_users.commit()
        print(f"Error: {e}")


@logger.catch()
@rate_limit(waiting_time, 'auth')
async def cmd_auth(message: types.Message):
    user_id = message.from_user.id
    current_time = time.time()
    user_text_list = message.text.split()

    if len(user_text_list) != 2:
        return

    user_input_email = user_text_list[1]

    cursor_users.execute('SELECT logged_in FROM logged WHERE user_id = %s', (user_id,))
    logged_in = cursor_users.fetchone()
    if logged_in is not None:
        logged_in = logged_in[0]
        if logged_in:
            await message.answer(text=msg.auth_already_logged_in_msg)
            return

    user_mail = is_valid_email(user_input_email)

    if not user_mail:
        await message.answer(msg.auth_incorrect_email_msg)
        return

    cursor_users.execute('SELECT logged_in FROM logged WHERE email = %s', (user_input_email,))
    logged_in = cursor_users.fetchone()
    if logged_in is not None:
        logged_in = logged_in[0]
        if logged_in:
            await message.answer(text=msg.auth_already_logged_in_email_msg)
            return

    cursor_users.execute('SELECT expiration FROM tempblocked WHERE user_id = %s', (user_id,))
    expiration_time = cursor_users.fetchone()
    if expiration_time is not None:
        expiration_time = expiration_time[0]
        current_time = time.time()

        if current_time < expiration_time:
            await message.answer(text=msg.auth_wrong_code_tempblock_msg)
            return
        else:
            try:
                cursor_users.execute('DELETE FROM tempblocked WHERE user_id = %s', (user_id,))
                cursor_users.execute('DELETE FROM auth WHERE user_id = %s', (user_id,))
                db_users.commit()
            except Exception as err:
                logger.critical(err)
                db_users.rollback()
                return

    cursor_users.execute('SELECT MAX(expiration) FROM auth WHERE user_id = %s', (user_id,))
    code_latest_expiration_time = cursor_users.fetchone()[0]

    if code_latest_expiration_time is not None:
        total_time = code_latest_expiration_time + send_code_delay

        if (current_time + code_expiration_time) < total_time:
            try:
                await message.answer(msg.auth_send_code_dely_msg.format(remain_time=round(total_time - current_time)))
                return
            except Exception as err:
                logger.critical(err)
                return

    email_code, encrypted_email_code = generate_and_encrypt_code()
    print(email_code, encrypted_email_code)

    try:
        cursor_users.execute('SELECT attempts FROM auth WHERE user_id = %s', (user_id,))
        total_attempts = cursor_users.fetchone()
        if total_attempts is None:
            total_attempts = max_attempts_code
        else:
            total_attempts = total_attempts[0]

        cursor_users.execute('INSERT INTO auth VALUES(%s, %s, %s, %s, %s)',
                             (user_id, encrypted_email_code, user_input_email, current_time + code_expiration_time, total_attempts))
        db_users.commit()

    except Exception as err:
        logger.error(err)
        db_users.rollback()
        await message.answer(msg.unknown_error_msg)
        return

    send_code_to_email(user_text_list[1], email_code, encrypted_email_code, user_id)

    logger.debug(f'{user_id} запросил код для авторизации.')

    try:
        await message.answer(msg.auth_send_email_success_msg.format(receiver_email=user_text_list[1]))
    except Exception as err:
        logger.critical(err)
