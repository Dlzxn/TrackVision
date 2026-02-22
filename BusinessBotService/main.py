import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import os
from dotenv import load_dotenv

# Загружаем .env
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Конфигурация
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env файле!")

# База данных в памяти (для простоты)
class Database:
    def __init__(self):
        self.users = {}  # user_id: {'registered': bool, 'name': str, 'date': str}
        self.codes = ["123456", "789012", "111111", "222333", "444555"]
        self.used_codes = set()
        self.stats = {
            'total_users': 0,
            'registered_users': 0,
            'start_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def check_code(self, code):
        return code in self.codes and code not in self.used_codes
    
    def use_code(self, code, user_id):
        if code in self.codes:
            self.used_codes.add(code)
            return True
        return False
    
    def add_user(self, user_id, username=None, first_name=None):
        if user_id not in self.users:
            self.users[user_id] = {
                'registered': False,
                'username': username,
                'first_name': first_name,
                'joined_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'messages_count': 0,
                'last_activity': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.stats['total_users'] += 1
            logger.info(f"Новый пользователь: {user_id}")
    
    def register_user(self, user_id):
        if user_id in self.users:
            self.users[user_id]['registered'] = True
            self.stats['registered_users'] += 1
            logger.info(f"Пользователь зарегистрирован: {user_id}")
    
    def update_activity(self, user_id):
        if user_id in self.users:
            self.users[user_id]['last_activity'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.users[user_id]['messages_count'] += 1
    
    def is_registered(self, user_id):
        return user_id in self.users and self.users[user_id]['registered']
    
    def get_user_info(self, user_id):
        if user_id in self.users:
            return self.users[user_id]
        return None
    
    def get_stats(self):
        uptime = datetime.now() - datetime.strptime(self.stats['start_time'], "%Y-%m-%d %H:%M:%S")
        return {
            'total': self.stats['total_users'],
            'registered': self.stats['registered_users'],
            'unregistered': self.stats['total_users'] - self.stats['registered_users'],
            'uptime': str(uptime).split('.')[0],
            'available_codes': len([c for c in self.codes if c not in self.used_codes])
        }

# Инициализация
db = Database()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Клавиатуры
def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Профиль"), KeyboardButton(text="ℹ️ Помощь")],
            [KeyboardButton(text="📈 Статистика"), KeyboardButton(text="🕒 Время")]
        ],
        resize_keyboard=True
    )
    return keyboard

# Состояния
class Registration(StatesGroup):
    waiting_for_code = State()

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    
    # Добавляем пользователя в БД
    db.add_user(user_id, username, first_name)
    
    if db.is_registered(user_id):
        await message.answer(
            f"👋 С возвращением, {first_name or 'друг'}!\n"
            f"Ты уже зарегистрирован и можешь пользоваться ботом.",
            reply_markup=get_main_keyboard()
        )
    else:
        await message.answer(
            "🔐 *Добро пожаловать!*\n\n"
            "Для доступа к боту необходимо ввести код.\n"
            "Пожалуйста, отправь код доступа:",
            parse_mode="Markdown"
        )
        await state.set_state(Registration.waiting_for_code)

# Обработка кода
@dp.message(Registration.waiting_for_code)
async def process_code(message: Message, state: FSMContext):
    code = message.text.strip()
    user_id = message.from_user.id
    
    # Проверка на команду
    if code.startswith('/'):
        await state.clear()
        await cmd_start(message, state)
        return
    
    # Проверяем код
    if db.check_code(code):
        # Используем код
        db.use_code(code, user_id)
        # Регистрируем пользователя
        db.register_user(user_id)
        db.update_activity(user_id)
        
        await message.answer(
            "✅ *Регистрация успешна!*\n\n"
            "Тебе доступны все функции бота.\n"
            "Используй кнопки ниже для навигации:",
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )
        await state.clear()
        
        # Отправляем приветственное сообщение
        await message.answer(
            f"🎉 Приятно познакомиться, {message.from_user.first_name or 'пользователь'}!\n"
            f"Твой ID: `{user_id}`\n"
            f"Код активации: `{code}`",
            parse_mode="Markdown"
        )
    else:
        await message.answer(
            "❌ *Неверный код!*\n\n"
            "Попробуй еще раз или введи /start для возврата в начало.",
            parse_mode="Markdown"
        )

# Обработка кнопки "Профиль"
@dp.message(lambda message: message.text == "📊 Профиль")
async def show_profile(message: Message):
    user_id = message.from_user.id
    
    if not db.is_registered(user_id):
        await message.answer("❌ Сначала зарегистрируйся через /start")
        return
    
    user_info = db.get_user_info(user_id)
    if user_info:
        status = "✅ Активен"
        reg_status = "✔ Зарегистрирован"
        
        profile_text = (
            f"👤 *Твой профиль*\n\n"
            f"🆔 ID: `{user_id}`\n"
            f"📝 Имя: {user_info['first_name'] or 'Не указано'}\n"
            f"🔰 Username: @{user_info['username'] or 'Не указан'}\n"
            f"📊 Статус: {reg_status}\n"
            f"⚡ Состояние: {status}\n"
            f"📅 Присоединился: {user_info['joined_date']}\n"
            f"💬 Сообщений: {user_info['messages_count']}\n"
            f"🕒 Последняя активность: {user_info['last_activity']}"
        )
        
        await message.answer(profile_text, parse_mode="Markdown")

# Обработка кнопки "Статистика"
@dp.message(lambda message: message.text == "📈 Статистика")
async def show_stats(message: Message):
    user_id = message.from_user.id
    
    if not db.is_registered(user_id):
        await message.answer("❌ Сначала зарегистрируйся через /start")
        return
    
    stats = db.get_stats()
    
    stats_text = (
        "📊 *Статистика бота*\n\n"
        f"👥 Всего пользователей: {stats['total']}\n"
        f"✅ Зарегистрировано: {stats['registered']}\n"
        f"⏳ Ожидают регистрацию: {stats['unregistered']}\n"
        f"🔢 Доступных кодов: {stats['available_codes']}\n"
        f"⏱ Аптайм: {stats['uptime']}"
    )
    
    await message.answer(stats_text, parse_mode="Markdown")

# Обработка кнопки "Помощь"
@dp.message(lambda message: message.text == "ℹ️ Помощь")
async def show_help(message: Message):
    user_id = message.from_user.id
    
    if not db.is_registered(user_id):
        await message.answer("❌ Сначала зарегистрируйся через /start")
        return
    
    help_text = (
        "📚 *Доступные команды*\n\n"
        "🔹 /start - Начать работу\n"
        "🔹 Кнопки меню:\n"
        "   • 📊 Профиль - информация о тебе\n"
        "   • 📈 Статистика - статистика бота\n"
        "   • ℹ️ Помощь - это сообщение\n"
        "   • 🕒 Время - текущее время\n\n"
        "📝 *Как пользоваться:*\n"
        "1. Отправь /start\n"
        "2. Введи код доступа\n"
        "3. Используй кнопки меню"
    )
    
    await message.answer(help_text, parse_mode="Markdown")

# Обработка кнопки "Время"
@dp.message(lambda message: message.text == "🕒 Время")
async def show_time(message: Message):
    user_id = message.from_user.id
    
    if not db.is_registered(user_id):
        await message.answer("❌ Сначала зарегистрируйся через /start")
        return
    
    current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    await message.answer(f"🕒 Текущее время: `{current_time}`", parse_mode="Markdown")

# Команда /help
@dp.message(Command("help"))
async def cmd_help(message: Message):
    await show_help(message)

# Команда /profile
@dp.message(Command("profile"))
async def cmd_profile(message: Message):
    await show_profile(message)

# Команда /stats
@dp.message(Command("stats"))
async def cmd_stats(message: Message):
    await show_stats(message)

# Команда /time
@dp.message(Command("time"))
async def cmd_time(message: Message):
    await show_time(message)

# Команда /codes (только для администратора)
@dp.message(Command("codes"))
async def show_codes(message: Message):
    user_id = message.from_user.id
    
    # Простая проверка на админа (можно заменить на свои ID)
    admin_ids = []  # Добавьте сюда свои ID через запятую
    if admin_ids and user_id not in admin_ids:
        await message.answer("⛔ У тебя нет прав для этой команды")
        return
    
    available = [c for c in db.codes if c not in db.used_codes]
    used = db.used_codes
    
    text = "🔢 *Коды доступа*\n\n"
    text += f"📌 Всего кодов: {len(db.codes)}\n"
    text += f"✅ Доступно: {len(available)}\n"
    text += f"❌ Использовано: {len(used)}\n\n"
    
    if available:
        text += "📋 *Свободные коды:*\n"
        text += "`" + "`, `".join(available) + "`"
    
    await message.answer(text, parse_mode="Markdown")

# Обработка обычных сообщений
@dp.message()
async def handle_message(message: Message):
    user_id = message.from_user.id
    text = message.text
    
    # Обновляем активность
    db.update_activity(user_id)
    
    if db.is_registered(user_id):
        # Эхо с дополнительной информацией
        response = (
            f"✉️ *Твое сообщение:*\n"
            f"`{text}`\n\n"
            f"📊 Длина: {len(text)} символов\n"
            f"🆔 ID сообщения: `{message.message_id}`"
        )
        await message.answer(response, parse_mode="Markdown")
    else:
        # Если не зарегистрирован, отправляем на регистрацию
        await message.answer("❌ Сначала зарегистрируйся через /start")

# Запуск бота
async def main():
    logger.info("=" * 50)
    logger.info("🚀 Бот запускается...")
    logger.info(f"🤖 Токен: {BOT_TOKEN[:10]}...")
    logger.info(f"📊 Доступные коды: {db.codes}")
    logger.info("=" * 50)
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
