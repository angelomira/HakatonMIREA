"""MIREA DORMITORY BOT CONFIG"""


# Основное
token = "6667439064:AAEfC6avvhwLqzLi6bc2UG_q50cqlS9WVIQ"  # Bot Token @BotFather

# Почта для отправки кодов
email_login = 'mireadormitorybot@mail.ru'
email_pass = 'FH2gKTWJ03wwfcbTCPAX'

owner_id = 435918797  # Айди владельца бота
admin_id_list = (435918797,)  # Айди админов бота
bot_name = "Общага МИРЭА"  # Никнейм бота
bot_username = "mirea_dormitory_bot"  # Юзернейм бота
bot_id = 6667439064  # id бота

# Чёрный список юзеров
black_list = (0,)  # Список с айди заблокированных в боте пользователей


# Данные для подключения к PostgreSQL
host_psql = '127.0.0.1'
user_psql = 'postgres'
password_psql = '123456'
db_name_psql = 'mirea_dormitory'
port_psql = 5432


# Данные для подключения к Redis
host_redis = '127.0.0.1'
port_redis = 6379
db_redis = 5
pool_size_redis = 300


waiting_time = 1  # Задержка на использование команд (в секундах). Default: 1
code_expiration_time = 300  # Время, через которое код авторизации истечёт (в секундах). Default: 300
send_code_delay = 60  # Время, через которое можно повторно запросить код (в секундах). Default: 60
session_expiration_time = 86400  # Время, в течение которого активна сессия. После, она станет неактивной. (в секундах). Default: 86400

enable_trades = True  # Включить или выключить трейды в боте.
enable_achievements = True  # Включить или выключить ачивки в боте.
enable_tickets_raffle = True  # Включить или выключить билетики розыгрыша.
raffle_require_level = 100  # Уровень, необходимый для участия в розыгрыше.
enable_halloween_event = True  # Включить или выключить хэллоуинский ивент.
enable_halloween_event_bosses = True  # Включить или выключить хэллоуинских боссов.
enable_items_materials = True  # Включить или выключить предметы с материалами.
