import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from database_handler import DatabaseHandler

class TelegramBot:
    def __init__(self, token_file):
        self.token = self.load_token(token_file)
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher(self.bot)
        self.db_handler = DatabaseHandler("database.db")

    def load_token(self, token_file):
        with open(token_file, "r") as file:
            return file.read().strip()

    async def on_start(self, message: types.Message):
        await message.answer("Привет! Добро пожаловать в наш конкурсный бот!")

    async def on_message(self, message: types.Message):
        # Здесь будет обработка сообщений от пользователя
        pass

    async def start_polling(self):
        # Регистрируем обработчики
        self.dp.register_message_handler(self.on_start, commands=['start'])
        self.dp.register_message_handler(self.on_message)

        # Запускаем бота
        await self.dp.start_polling()

    async def shutdown(self, dp):
        await dp.storage.close()
        await dp.storage.wait_closed()

    def start(self):
        asyncio.run(self.start_polling())

if __name__ == "__main__":
    bot = TelegramBot("token.txt")
    bot.start()
