from database.connect import cursor_users
import messages as msg


async def check_logged_in_fun(message, user_id):
    cursor_users.execute('SELECT logged_in FROM logged WHERE user_id = %s', (user_id,))
    user_info = cursor_users.fetchone()
    if user_info is not None:
        logged_in = user_info[0]
        if not logged_in:
            await message.answer(text=msg.auth_need_msg)
            return True
    else:
        await message.answer(text=msg.auth_need_msg)
        return True
