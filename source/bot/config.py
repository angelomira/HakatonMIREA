"""MIREA DORMITORY BOT CONFIG"""


# Основное
token = "6667439064:AAEfC6avvhwLqzLi6bc2UG_q50cqlS9WVIQ"  # Bot Token @BotFather

# Почта для отправки кодов
email_login = 'mireadormitorybot@mail.ru'
email_pass = 'FH2gKTWJ03wwfcbTCPAX'

# Подключение по вебхуку (отключено)
# WEBHOOK_HOST = '65.108.32.53'  # Домен, на который Телеграм будет отправлять обновления
# WEBHOOK_PORT = 8443
# WEBHOOK_PATH = '/bot'  # Путь на сервере, по которому будут приходить обновления
# WEBHOOK_URL = f"https://{WEBHOOK_HOST}:{WEBHOOK_PORT}{WEBHOOK_PATH}"
#
#
# WEBAPP_HOST = 'localhost'
# WEBAPP_PORT = 8443
#
# WEBHOOK_SSL_CERT = "/home/mine_evo_test/webhook.pem"
# WEBHOOK_SSL_PRIV = "/home/mine_evo_test/webhook.key"

owner_id = 435918797  # Айди владельца бота
admin_id_list = (435918797, 1041161677, 1153403818, 5555473380)  # Айди админов бота
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
max_attempts_code = 5  # Максимальное кол-во попыток для ввода кода. Default: 5
temblock_time = 7200  # Время, которое нужно будет подождать, прежде чем снова попробовать ввести код. Default: 7200
