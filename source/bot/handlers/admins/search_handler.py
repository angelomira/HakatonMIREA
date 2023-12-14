import datetime
import re

from aiogram import types
from loguru import logger

import messages as msg
from config import waiting_time
from database.connect import cursor_users
from utils.antiflood import rate_limit
from utils.check_logged_in import check_logged_in_fun

ANTIFLOOD_TIME = 1


def is_valid_code(code):
    pattern = r'^\d{6}$'
    if re.match(pattern, code):
        return True
    else:
        return False


async def get_student_info(message, student_card_id):
    cursor_users.execute('SELECT id, user_id, first_name, middle_name, last_name, birth_date, dormitory_prov_order, enrollment_order, '
                         'birth_place, residential_address FROM student_card WHERE id = %s', (student_card_id,))
    student_info = cursor_users.fetchone()
    if student_info is not None:
        card_id = student_info[0]
        student_id = student_info[1]
        first_name = student_info[2]
        middle_name = student_info[3]
        last_name = student_info[4]
        birth_date = student_info[5]
        dormitory_prov_order = student_info[6]
        enrollment_order = student_info[7]
        birth_place = student_info[8]
        residential_address = student_info[9]

        name = f'{last_name.capitalize()} {first_name.capitalize()} {middle_name.capitalize()}'

        cursor_users.execute('SELECT building, storey, room, check_in_date FROM occupied_rooms WHERE user_id = %s', (student_id,))
        student_dormitory_info = cursor_users.fetchone()
        if student_dormitory_info is not None:
            building = student_dormitory_info[0]
            storey = student_dormitory_info[1]
            room = student_dormitory_info[2]
            check_in_time = student_dormitory_info[3]

            check_in_time = datetime.datetime.fromtimestamp(check_in_time).strftime('%d-%m-%Y в %H:%M:%S')

            dormitory_stident_info = f'Да.\n' \
                                     f'Корпус здания: {building}\n' \
                                     f'Этаж: {storey}\n' \
                                     f'Комната: {room}\n' \
                                     f'Дата заселения: {check_in_time}'
        else:
            dormitory_stident_info = 'Нет.'

        await message.answer(text=msg.search_student_found_msg.format(card_id=card_id,
                                                                      student_id=student_id,
                                                                      name=name,
                                                                      birth_date=birth_date,
                                                                      dormitory_prov_order=dormitory_prov_order,
                                                                      enrollment_order=enrollment_order,
                                                                      birth_place=birth_place,
                                                                      residential_address=residential_address,
                                                                      dormitory_stident_info=dormitory_stident_info))

    else:
        await message.answer(text=msg.search_student_not_found_msg)
        return


@logger.catch()
@rate_limit(waiting_time, 'search')
async def cmd_search(message: types.Message):
    user_msg = message.text.split()
    user_id = message.from_user.id

    if await check_logged_in_fun(message, user_id):
        return

    if len(user_msg) == 2:
        try:
            student_card_id = int(user_msg[1])
        except Exception as err:
            await message.answer(text=msg.search_error_id_msg)
            logger.error(err)
            return

        cursor_users.execute('SELECT id FROM student_card WHERE id = %s', (student_card_id,))
        student_info = cursor_users.fetchone()
        if student_info is not None:
            student_card_id = student_info[0]
            await get_student_info(message, student_card_id)
            return
        else:
            await message.answer(text=msg.search_student_not_found_msg)
            return

    elif len(user_msg) == 4:
        try:
            building = int(user_msg[1])
            storey = int(user_msg[2])
            room = int(user_msg[3])

            cursor_users.execute('SELECT user_id FROM occupied_rooms WHERE building = %s AND storey = %s AND room = %s',
                                 (building, storey, room))
            student_info = cursor_users.fetchone()
            if student_info is not None:
                student_id = student_info[0]
                cursor_users.execute('SELECT id FROM student_card WHERE user_id = %s',
                                     (student_id,))
                student_card_id = cursor_users.fetchone()[0]

                await get_student_info(message, student_card_id)
                return
            else:
                await message.answer(text=msg.search_student_not_found_msg)
                return

        except Exception as err:
            logger.warning(err)

        try:
            last_name = user_msg[1].lower()
            first_name = user_msg[2].lower()
            middle_name = user_msg[3].lower()

            cursor_users.execute('SELECT id FROM student_card WHERE first_name = %s AND middle_name = %s AND last_name = %s',
                                 (first_name, middle_name, last_name))
            student_info = cursor_users.fetchone()
            if student_info is not None:
                student_card_id = student_info[0]
                await get_student_info(message, student_card_id)
                return
            else:
                await message.answer(text=msg.search_student_not_found_msg)
                return

        except Exception as err:
            await message.answer(text=msg.unknown_error_msg)
            logger.error(err)
            return

    else:
        await message.answer(text=msg.search_help_msg)
        return
