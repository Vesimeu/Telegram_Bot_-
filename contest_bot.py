import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from database_handler import DatabaseHandler
from utils import is_vk_link
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage


class QuizState(StatesGroup):
    QUESTION = State()
    ANSWER = State()
    PHOTO = State()

class TelegramBot:
    def __init__(self, token_file):
        storage = MemoryStorage()
        self.token = self.load_token(token_file)
        self.bot = Bot(token=self.token)
        self.dp = Dispatcher(self.bot, storage=storage)
        self.db_handler = DatabaseHandler("database.db")
        self.district_codes = {
            "01": "Александровский муниципальный округ",
            "02": "Бардымский муниципальный округ",
            "03": "Берёзовский муниципальный округ",
            "04": "Березниковский городской округ",
            "05": "Большесосновский муниципальный округ",
            "06": "Верещагинский городской округ",
            "07": "Гайнский муниципальный округ",
            "08": "Горнозаводский городской округ",
            "09": "Губахинский муниципальный округ",
            "10": "Добрянский городской округ",
            "11": "Еловский муниципальный округ",
            "12": "ЗАТО Звёздный",
            "13": "Ильинский городской округ",
            "14": "Карагайский муниципальный округ",
            "15": "Кизеловский городской округ",
            "16": "Кишертский муниципальный округ",
            "17": "Косинский муниципальный округ",
            "18": "Кочёвский муниципальный округ",
            "19": "Красновишерский городской округ",
            "20": "Краснокамский городской округ",
            "21": "Кудымкарский муниципальный округ",
            "22": "Куединский муниципальный округ",
            "23": "Кунгурский муниципальный округ",
            "24": "Лысьвенский городской округ",
            "25": "Нытвенский городской округ",
            "26": "Октябрьский городской округ",
            "27": "Ординский муниципальный округ",
            "28": "Осинский городской округ",
            "29": "Оханский городской округ",
            "30": "Очёрский городской округ",
            "31": "Пермский городской округ",
            "32": "Пермский муниципальный округ",
            "33": "Сивинский муниципальный округ",
            "34": "Соликамский городской округ",
            "35": "Суксунский городской округ",
            "36": "Уинский муниципальный округ",
            "37": "Чайковский городской округ",
            "38": "Частинский муниципальный округ",
            "39": "Чердынский городской округ",
            "40": "Чернушинский городской округ",
            "41": "Чусовской городской округ",
            "42": "Юрлинский муниципальный округ",
            "43": "Юсьвинский муниципальный округ"
        }

    def load_token(self, token_file):
        with open(token_file, "r") as file:
            return file.read().strip()

    async def on_start(self, message: types.Message, state: FSMContext):
        await message.answer("Привет! Добро пожаловать в наш конкурсный бот!")
        await self.stage_0(message, state)

    async def on_message(self, message: types.Message, state: FSMContext):
        if message.text == '/start':
            await self.on_start(message, state)
        elif message.text == '/stage1':
            await self.stage_0(message, state)
        # Добавляем обработку других этапов конкурса
        # elif message.text == '/stage2':
        #     await self.stage_2(message, state)
        # elif message.text == '/stage3':
        #     await self.stage_3(message, state)
        # и так далее
        else:
            await message.answer(
                "Я не понимаю вашего сообщения. Для начала конкурса введите /start. Для перехода к определенному этапу введите соответствующую команду.")

    async def start_polling(self):
        # Регистрируем обработчики
        self.dp.register_message_handler(self.on_start, commands=['start'])
        # self.dp.register_message_handler(self.on_message)

        # Запускаем бота
        await self.dp.start_polling()

    async def shutdown(self, dp):
        await dp.storage.close()
        await dp.storage.wait_closed()

    def start(self):
        asyncio.run(self.start_polling())

    async def stage_0(self, message: types.Message, state: FSMContext):
        user_id = str(message.from_user.id)

        # Проверяем, зарегистрирован ли уже пользователь
        if self.db_handler.is_user_registered(user_id):
            await message.answer("Вы уже зарегистрированы. Для продолжения конкурса введите /start.")
            return

        # Выводим список муниципальных округов
        districts_list = "\n".join([f"{code}: {district}" for code, district in self.district_codes.items()])
        await message.answer("Выберите свой муниципальный округ, введя соответствующий код:\n\n" + districts_list)

        # Регистрируем обработчик для этапа выбора муниципального округа
        @self.dp.message_handler(content_types=types.ContentType.TEXT, state="*")
        async def process_district_code(message: types.Message, state: FSMContext):
            district_code = message.text.strip()

            # Проверяем, что введенный код действителен
            if district_code not in self.district_codes.keys():
                await message.answer("Неверный код муниципального округа. Пожалуйста, попробуйте снова.")
                return

            # Записываем данные в базу данных
            user_id = str(message.from_user.id)
            district_name = self.district_codes[district_code]
            self.db_handler.add_user(user_id, district_name)

            await message.answer("Спасибо! Вы успешно зарегистрировались. Теперь приступим к первому этапу конкурса.")

            # Удаляем обработчик после завершения этапа выбора муниципального округа
            self.dp.message_handlers.unregister(process_district_code)

            # Переходим к первому этапу конкурса
            await self.stage_1(message, state)

        await state.finish()

    async def stage_1(self, message: types.Message, state: FSMContext):
        await message.answer("Добро пожаловать на первый этап конкурса!")

        # Задаем вопрос и ждем ответа с ссылкой на видео в формате VK
        await message.answer("Сними видео до 1 минуты с ответом на вопрос: «Что для меня Движение Первых?» "
                             "Размести ролик на своей странице ВК/сообществе отделения с тегами #ДвижениеПервых59 #КвестОтделений59. "
                             "Проследи, чтобы страничка была открытой! Отправь ссылку на свой ролик нашему чат-боту.")

        # Ожидаем ответа пользователя
        @self.dp.message_handler(content_types=types.ContentType.TEXT, state=QuizState.QUESTION)
        async def process_video_link(message: types.Message, state: FSMContext):
            video_link = message.text.strip()

            # Проверяем, является ли ссылка ссылкой из ВК
            if not is_vk_link(video_link):
                await message.answer("Неверный формат ссылки. Пожалуйста, отправьте ссылку на видео из ВКонтакте.")
                return

            # Добавляем ссылку в базу данных
            user_id = str(message.from_user.id)
            self.db_handler.add_video_link(user_id, video_link)
            self.db_handler.add_points(user_id, 5)

            await message.answer("Спасибо! Ваша ссылка на видео успешно добавлена. Переходим к следующему этапу.")

            # Переходим ко второму этапу конкурса
            await self.stage_2(message, state)

        await QuizState.QUESTION.set()

    async def stage_2(self, message: types.Message, state: FSMContext):
        await message.answer("Добро пожаловать на второй этап конкурса!")

        # Задаем вопрос и ждем ответа с ссылкой на фотографию отделения в формате VK
        await message.answer(
            "Сделайте креативную фотографию своего первичного отделения. На фотографии должны быть представлены участники и ваш председатель. "
            "Опубликуйте её на своей странице ВК/сообществе отделения с хэштегами #ДвижениеПервых59 #КвестОтделений59. "
            "Проследите, чтобы страничка была открытой! Отправьте ссылку на пост с фото нашему чат-боту.")

        # Ожидаем ответа пользователя
        @self.dp.message_handler(content_types=types.ContentType.TEXT, state=QuizState.PHOTO)
        async def process_photo_link(message: types.Message, state: FSMContext):
            photo_link = message.text.strip()

            # Проверяем, является ли ссылка ссылкой из ВК
            if not is_vk_link(photo_link):
                await message.answer("Неверный формат ссылки. Пожалуйста, отправьте ссылку на фотографию из ВКонтакте.")
                return

            # Добавляем ссылку в базу данных
            user_id = str(message.from_user.id)
            self.db_handler.add_photo_link(user_id, photo_link)
            self.db_handler.add_points(user_id, 5)

            await message.answer("Спасибо! Ваша ссылка на фотографию успешно добавлена. Переходим к следующему этапу.")

            # Переходим к третьему этапу конкурса
            await self.stage_3(message, state)

        await QuizState.PHOTO.set()

    async def stage_3(self, message: types.Message, state: FSMContext):
        await message.answer("Добро пожаловать на третий этап конкурса! Вас ждет викторина.")

        questions = [
            {
                "question": "Какие технологии используются для создания искусственного интеллекта?",
                "options": ["нейронные сети", "машинное обучение", "искусственные нейроны", "квантовые компьютеры"],
                "correct_answer": "нейронные сети"
            },
            # Добавьте остальные вопросы аналогичным образом
        ]

        async def ask_question(question, options):
            message_text = f"{question}\n\n"
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for option in options:
                keyboard.add(types.KeyboardButton(option))
                message_text += f"- {option}\n"
            await message.answer(message_text, reply_markup=keyboard)
            await QuizState.ANSWER.set()

        async def process_answer(answer, correct_answer):
            if answer == correct_answer:
                self.db_handler.add_points(str(message.from_user.id), 1)
                await message.answer("Верно! Вы получаете 1 балл.")
            else:
                await message.answer("Неверно. Правильный ответ: " + correct_answer)
            await QuizState.QUESTION.set()

        async def process_answer_msg(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                question_idx = data.get('question_idx')
                question = questions[question_idx]
                await process_answer(message.text.strip(), question['correct_answer'])
                if question_idx + 1 < len(questions):
                    await ask_question(questions[question_idx + 1]["question"], questions[question_idx + 1]["options"])
                    data['question_idx'] = question_idx + 1
                else:
                    await message.answer("Викторина завершена. Переходим к следующему этапу.")
                    # await self.stage_4(message)
            await state.finish()

        async with state.proxy() as data:
            data['question_idx'] = 0
        await ask_question(questions[0]["question"], questions[0]["options"])

        self.dp.register_message_handler(process_answer_msg, state=QuizState.ANSWER)


if __name__ == "__main__":
    bot = TelegramBot("token.txt")
    bot.start()
