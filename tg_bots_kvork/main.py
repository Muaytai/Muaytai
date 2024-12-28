from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes
from typing import Dict, Any
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import sqlite3

# Загружаем переменные окружения
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')
CHANNEL_ID = os.getenv('CHANNEL_ID')

# Состояния для FSM
class States:
    REGISTRATION = "registration"
    CONTACT = "contact"
    CITY = "city"
    CREATE_AD = "create_ad"
    AD_TYPE = "ad_type"
    AD_CITY = "ad_city"
    AD_CONTENT = "ad_content"
    AD_IMAGE = "ad_image"
    AD_SALARY = "ad_salary"
    AD_HASHTAGS = "ad_hashtags"

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('board.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            city TEXT,
            balance REAL DEFAULT 0,
            is_verified BOOLEAN DEFAULT FALSE,
            last_free_post TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало работы с ботом"""
    user_id = update.message.from_user.id
    
    # Проверка подписки на канал
    member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
    if member.status in ['left', 'kicked']:
        keyboard = [[InlineKeyboardButton("Подписаться на канал", url=f"https://t.me/{CHANNEL_ID}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Для использования бота необходимо подписаться на канал!",
            reply_markup=reply_markup
        )
        return States.REGISTRATION

    # Запрос контакта
    keyboard = [[InlineKeyboardButton("Поделиться контактом", request_contact=True)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Для регистрации поделитесь своим контактом",
        reply_markup=reply_markup
    )
    return States.CONTACT

async def get_updates(offset: int = None) -> Dict[str, Any]:
    """Получает обновления от Telegram API"""
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates'
    params = {'timeout': 30}
    if offset:
        params['offset'] = offset
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params) as response:
                return await response.json()
        except Exception as e:
            print(f"Ошибка при получении обновлений: {e}")
            return {}

async def send_message(chat_id: int, text: str) -> None:
    """Отправляет сообщение пользователю"""
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': text
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=data) as response:
                await response.json()
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")

async def main():
    offset = None
    while True:
        updates = await get_updates(offset)
        if 'result' in updates:
            for update in updates['result']:
                message = update.get('message', {})
                chat_id = message.get('chat', {}).get('id')
                text = message.get('text', '')

                if text == '/start':
                    await send_message(chat_id, "Привет! Я бот для знакомства с Telegram API.")
                
                offset = update['update_id'] + 1

if __name__ == "__main__":
    asyncio.run(main())
