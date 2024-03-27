from aiogram import Bot, Dispatcher, types
import asyncio
import sqlite3


def load_token(token_file):
    with open(token_file, "r") as file:
        return file.read().strip()


API_TOKEN = load_token("token.txt")

# Создаем объект бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Функция для рассылки сообщений
# Функция для получения списка всех пользователей из базы данных
def get_all_users():
    connection = sqlite3.connect('database.db')  # Подставьте имя вашей базы данных
    cursor = connection.cursor()
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    connection.close()
    return [user[0] for user in users]

# Функция для рассылки сообщений
async def send_message_to_all_users(message: str):
    users = get_all_users()  # Получаем всех пользователей из базы данных

    for user_id in users:
        try:
            await bot.send_message(user_id, message)
            print(f"Сообщение отправлено пользователю {user_id}")
        except Exception as e:
            print(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")

async def main():
    message = "И да, теперь через этого бота можно будет отправлять сообщения тем, кто зарегистрирован в базе данных =)."
    await send_message_to_all_users(message)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
