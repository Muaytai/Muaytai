import asyncio
import aiohttp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, 
    MessageHandler, filters, ContextTypes, ConversationHandler
)
from typing import Dict, Any
import os
from dotenv import load_dotenv
import sqlite3
from datetime import datetime, timedelta
import re

load_dotenv()

# Константы для токенов
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))
CHANNEL_ID = os.getenv('CHANNEL_ID')

# Состояния регистрации
CONTACT = 1
CITY = 2
VERIFICATION_CHOICE = 3

# Состояния создания объявления
CHOOSE_TYPE = 4
CHOOSE_CITY = 5
CONTENT = 6
IMAGE = 7
SALARY = 8
HASHTAGS = 9
CONFIRMATION = 10

# Добавьте новые состояния после существующих
PROFILE_MENU = 11
CHANGE_CITY = 12
ADD_BALANCE = 13
TRANSFER_BALANCE = 14
MY_ADS = 15

# Добавьте новые состояния после существующих
SEARCH_MENU = 16
SEARCH_TYPE = 17
SEARCH_CITY = 18
SEARCH_HASHTAG = 19
SEARCH_PRICE = 20

AD_TYPES = {
    "⭐️ ВОПРОС ⭐️": {"price": 0, "code": "question"},
    "💎 БАРАХОЛКА 💎": {"price": 0, "code": "market"},
    "👨‍💼 ВАКАНСИИ 👩‍💼": {"price": 0, "code": "job"},
    "🏢 НЕДВИЖИМОСТЬ 🏠": {"price": 0, "code": "realty"},
    "🚗 АВТО-МОТО 🏍": {"price": 0, "code": "auto"},
    "🐾 ЖИВОТНЫЕ 🌺": {"price": 0, "code": "pets"},
    "✨ УСЛУГИ ✨": {"price": 10000, "code": "services"},
    "💫 ДЛЯ БИЗНЕСА 💫": {"price": 15000, "code": "business"}
}

ALLOWED_DOMAINS = [
    "facebook.com",
    "instagram.com",
    "vk.com",
    "ok.ru"
]

def init_db():
    """Инициализация базы данных"""
    conn = sqlite3.connect('board.db')
    c = conn.cursor()
    
    # Таблица пользователей
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            phone TEXT,
            city TEXT,
            balance REAL DEFAULT 0,
            is_verified BOOLEAN DEFAULT FALSE,
            verification_requested BOOLEAN DEFAULT FALSE,
            last_free_post TIMESTAMP,
            registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Таблица городов
    c.execute('''
        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    ''')
    
    # Таблица объявлений
    c.execute('''
        CREATE TABLE IF NOT EXISTS ads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            type TEXT,
            city TEXT,
            content TEXT,
            image_file_id TEXT,
            salary TEXT,
            hashtags TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    conn.commit()
    conn.close()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало работы с ботом"""
    # Проверяем, что это личный чат
    if update.effective_chat.type != 'private':
        await update.message.reply_text(
            "Пожалуйста, начните диалог со мной в личных сообщениях:\n"
            "@tgkvork_bot"
        )
        return ConversationHandler.END
        
    user_id = update.effective_user.id
    
    # Проверяем, зарегистрирован ли пользователь
    conn = sqlite3.connect('board.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    
    if user:
        await show_main_menu(update, context)
        return ConversationHandler.END
    
    # Проверка подписки на канал
    try:
        if not CHANNEL_ID:
            print("CHANNEL_ID не настроен")
            raise ValueError("CHANNEL_ID не настроен")
            
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if member.status in ['left', 'kicked']:
            channel_link = CHANNEL_ID[4:] if CHANNEL_ID.startswith('-100') else CHANNEL_ID
            keyboard = [[InlineKeyboardButton("Подписаться на канал", url=f"https://t.me/{channel_link}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                "Для использования бота необходимо подписаться на канал!",
                reply_markup=reply_markup
            )
            return ConversationHandler.END
    except Exception as e:
        print(f"Ошибка при проверке подписки: {e}")
        # Временно пропускаем проверку подписки при ошибке
        pass

    # Запрос контакта
    keyboard = [[KeyboardButton("Поделиться контактом", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Для регистрации поделитесь своим контактом",
        reply_markup=reply_markup
    )
    return CONTACT

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает главное меню"""
    keyboard = [
        ["🌟 СОЗДАТЬ ОБЪЯВЛЕНИЕ ✨", "🔍 ПОИСК ОБЪЯВЛЕНИЙ 🎯"],
        ["📹 ВИДЕО-ИНСТРУКЦИЯ 🎥", "👤 МОЙ ПРОФИЛЬ 💫"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "✨ Выберите действие:",
        reply_markup=reply_markup
    )

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка полученного контакта"""
    contact = update.message.contact
    user_id = update.effective_user.id
    
    if contact.user_id != user_id:
        await update.message.reply_text(
            "Пожалуйста, поделитесь своим контактом, а не чужим.",
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton("Поделиться контактом", request_contact=True)]], 
            resize_keyboard=True)
        )
        return CONTACT
    
    # Сохраняем контакт во временных данных
    context.user_data['phone'] = contact.phone_number
    
    # Получаем список городов из базы
    conn = sqlite3.connect('board.db')
    c = conn.cursor()
    c.execute("SELECT name FROM cities ORDER BY name")
    cities = c.fetchall()
    conn.close()
    
    if not cities:
        # Если список городов пуст, добавляем базовые города
        default_cities = ["Сеул", "Пусан", "Инчхон", "Тэгу", "Тэдон", "Квандж", "Ульсан"]
        conn = sqlite3.connect('board.db')
        c = conn.cursor()
        for city in default_cities:
            c.execute("INSERT OR IGNORE INTO cities (name) VALUES (?)", (city,))
        conn.commit()
        cities = [(city,) for city in default_cities]
        conn.close()
    
    # Создаем клавиатуру с городами
    keyboard = [[city[0]] for city in cities]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "Выберите ваш город:",
        reply_markup=reply_markup
    )
    return CITY

async def handle_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка выбранного города"""
    city = update.message.text
    user_id = update.effective_user.id
    username = update.effective_user.username
    phone = context.user_data.get('phone')
    
    # Проверяем, существует ли город в базе
    conn = sqlite3.connect('board.db')
    c = conn.cursor()
    c.execute("SELECT name FROM cities WHERE name = ?", (city,))
    if not c.fetchone():
        await update.message.reply_text(
            "Пожалуйста, выберите город из списка."
        )
        conn.close()
        return CITY

    # Проверяем, существует ли пользователь
    c.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    user_exists = c.fetchone()
    
    if user_exists:
        # Если пользователь существует, обновляем его данные
        c.execute("""
            UPDATE users 
            SET username = ?, phone = ?, city = ?
            WHERE user_id = ?
        """, (username, phone, city, user_id))
    else:
        # Если пользователь новый, создаем запись
        c.execute("""
            INSERT INTO users (user_id, username, phone, city)
            VALUES (?, ?, ?, ?)
        """, (user_id, username, phone, city))
    
    conn.commit()
    conn.close()
    
    # Предлагаем верификацию
    keyboard = [
        [InlineKeyboardButton("Да, хочу верификацию", callback_data="verify_yes")],
        [InlineKeyboardButton("Нет, пропустить", callback_data="verify_no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Регистрация успешно завершена! 🎉\n\n"
        "Хотите пройти верификацию для специалистов и представителей бизнеса?\n"
        "Это даст вам дополнительные возможности и отметку ✅ на ваших объявлениях.",
        reply_markup=reply_markup
    )
    return VERIFICATION_CHOICE

async def handle_verification_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка выбора верификации"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "verify_yes":
        conn = sqlite3.connect('board.db')
        c = conn.cursor()
        c.execute("""
            UPDATE users 
            SET verification_requested = TRUE 
            WHERE user_id = ?
        """, (query.from_user.id,))
        conn.commit()
        conn.close()
        
        await query.edit_message_text(
            "Запрос на верификацию отправлен администратору. "
            "Мы свяжемся с вами для уточнения деталей.\n\n"
            "Стоимость верификации: 50,000 KRW"
        )
        
        # Показываем главное меню через новое сообщение
        keyboard = [
            ["🌟 СОЗДАТЬ ОБЪЯВЛЕНИЕ ✨", "🔍 ПОИСК ОБЪЯВЛЕНИЙ 🎯"],
            ["📹 ВИДЕО-ИНСТРУКЦИЯ 🎥", "👤 МОЙ ПРОФИЛЬ 💫"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await context.bot.send_message(
            chat_id=query.from_user.id,
            text="✨ Выберите действие:",
            reply_markup=reply_markup
        )
    else:
        await query.edit_message_text(
            "Вы всегда можете запросить верификацию позже в своем профиле."
        )
        # Показываем главное меню через новое сообщение
        keyboard = [
            ["🌟 СОЗДАТЬ ОБЪЯВЛЕНИЕ ✨", "🔍 ПОИСК ОБЪЯВЛЕНИЙ 🎯"],
            ["📹 ВИДЕО-ИНСТРУКЦИЯ 🎥", "👤 МОЙ ПРОФИЛЬ 💫"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await context.bot.send_message(
            chat_id=query.from_user.id,
            text="✨ Выберите действие:",
            reply_markup=reply_markup
        )
    
    return ConversationHandler.END

async def create_ad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало создания объявления"""
    user_id = update.effective_user.id
    
    # Проверяем, может ли пользователь создать бесплатное объявление
    conn = sqlite3.connect('board.db')
    c = conn.cursor()
    c.execute("""
        SELECT last_free_post, is_verified 
        FROM users 
        WHERE user_id = ?
    """, (user_id,))
    user_data = c.fetchone()
    conn.close()
    
    if user_data:
        last_post, is_verified = user_data
        if last_post:
            last_post_time = datetime.fromisoformat(last_post)
            if datetime.now() - last_post_time < timedelta(hours=3) and not is_verified:
                await update.message.reply_text(
                    "Вы можете создавать бесплатные объявления раз в 3 часа.\n"
                    "Дождитесь окончания таймера или пройдите верификацию."
                )
                return ConversationHandler.END
    
    # Создаем клавиатуру с типами объявлений
    keyboard = [[type_name] for type_name in AD_TYPES.keys()]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "Выберите тип объявления:",
        reply_markup=reply_markup
    )
    return CHOOSE_TYPE

async def handle_ad_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка выбранного типа объявления"""
    ad_type = update.message.text
    user_id = update.effective_user.id
    
    if ad_type not in AD_TYPES:
        await update.message.reply_text("Пожалуйста, выберите тип объявления из списка.")
        return CHOOSE_TYPE
    
    # Проверяем, является ли пользователь верифицированным для платных категорий
    if AD_TYPES[ad_type]["price"] > 0:
        conn = sqlite3.connect('board.db')
        c = conn.cursor()
        c.execute("SELECT is_verified, balance FROM users WHERE user_id = ?", (user_id,))
        user_data = c.fetchone()
        conn.close()
        
        if not user_data[0]:  # не верифицирован
            await update.message.reply_text(
                "Для размещения платных объявлений необходима верификация.\n"
                "Перейдите в профиль для получения верификации."
            )
            return ConversationHandler.END
        
        if user_data[1] < AD_TYPES[ad_type]["price"]:  # недостаточно средств
            await update.message.reply_text(
                f"Недостаточно средств. Необходимо: {AD_TYPES[ad_type]['price']} KRW\n"
                "Пополните баланс в профиле."
            )
            return ConversationHandler.END
    
    # Сохраняем тип объявления
    context.user_data['ad_type'] = ad_type
    
    # Получаем список городов
    conn = sqlite3.connect('board.db')
    c = conn.cursor()
    c.execute("SELECT name FROM cities ORDER BY name")
    cities = c.fetchall()
    conn.close()
    
    # Создаем клавиатуру с городами
    keyboard = [[city[0]] for city in cities]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "Выберите город для объявления:",
        reply_markup=reply_markup
    )
    return CHOOSE_CITY

async def handle_city_for_ad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка выбранного города для объявления"""
    city = update.message.text
    
    # Проверяем, существует ли город в базе
    conn = sqlite3.connect('board.db')
    c = conn.cursor()
    c.execute("SELECT name FROM cities WHERE name = ?", (city,))
    if not c.fetchone():
        await update.message.reply_text(
            "Пожалуйста, выберите город из списка."
        )
        return CHOOSE_CITY
    conn.close()
    
    # Сохраняем город
    context.user_data['ad_city'] = city
    
    # Запрашиваем текст объявления
    await update.message.reply_text(
        "Введите текст вашего объявления:\n\n"
        "❗️ Правила:\n"
        "1. Разрешены ссылки только на соцсети\n"
        "2. Запрещена реклама других каналов/групп\n"
        "3. Текст должен быть информативным\n\n"
        "Для отмены используйте /cancel"
    )
    return CONTENT

def check_links(text: str) -> bool:
    """Проверка ссылок в тексте"""
    # Находим все URL в тексте
    urls = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[^\s]*', text)
    
    for url in urls:
        # Проверяем, начинается ли URL с разрешенного домена
        allowed = False
        for domain in ALLOWED_DOMAINS:
            if domain in url.lower():
                allowed = True
                break
        if not allowed:
            return False
    return True

async def handle_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка текста объявления"""
    content = update.message.text
    
    # Проверяем ссылки
    if not check_links(content):
        await update.message.reply_text(
            "⚠️ В тексте найдены запрещенные ссылки!\n\n"
            "Разрешены ссылки только на следующие сайты:\n" +
            "\n".join(f"- {domain}" for domain in ALLOWED_DOMAINS) +
            "\n\nПожа��уйста, исправьте текст и отправьте снова."
        )
        return CONTENT
    
    # Сохраняем текст
    context.user_data['ad_content'] = content
    
    # Запрашиваем изображение
    keyboard = [["Пропустить"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "Отправьте одно изображение для объявления\n"
        "или нажмите 'Пропустить'",
        reply_markup=reply_markup
    )
    return IMAGE

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка загруженного изображения"""
    # Сохраняем file_id изображения
    photo = update.message.photo[-1]  # Берем последнее (самое качественное) изображение
    context.user_data['image_file_id'] = photo.file_id
    
    # Если тип объявления - вакансия, запрашиваем зарплату
    if context.user_data['ad_type'] == "👷‍💼 ВАКАНСИИ 👩‍💼":
        keyboard = [
            ["В час", "В день", "В неделю"],
            ["В месяц", "В год", "Сдельно"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "Укажите период выплаты зарплаты:",
            reply_markup=reply_markup
        )
        return SALARY
    else:
        return await request_hashtags(update, context)

async def skip_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Пропуск загрузки изображения"""
    context.user_data['image_file_id'] = None
    
    if context.user_data['ad_type'] == "👷‍💼 ВАКАНСИИ 👩‍💼":
        keyboard = [
            ["В час", "В день", "В неделю"],
            ["В месяц", "В год", "Сдельно"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "Укажите период выплаты зарплаты:",
            reply_markup=reply_markup
        )
        return SALARY
    else:
        return await request_hashtags(update, context)

async def handle_salary_period(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка периода выплаты зарплаты"""
    period = update.message.text
    context.user_data['salary_period'] = period
    
    keyboard = [["Указать диапазон"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "Укажите размер зарплаты (в KRW)\n"
        "Например: 2500000\n"
        "Или нажмите 'Указать диапазон'",
        reply_markup=reply_markup
    )
    return SALARY + 1  # Дополнительное состояние для суммы

async def handle_salary_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка суммы зарплаты"""
    text = update.message.text
    
    if text == "Указать диапазон":
        await update.message.reply_text(
            "Укажите минимальную сумму зарплаты (в KRW):"
        )
        context.user_data['salary_range'] = True
        return SALARY + 2  # Состояние для минимальной суммы
    
    try:
        amount = int(text)
        context.user_data['salary'] = f"{amount:,} KRW {context.user_data['salary_period']}"
        return await request_hashtags(update, context)
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите числовое значение.")
        return SALARY + 1

async def handle_salary_min(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка минимальной суммы зарплаты"""
    try:
        min_amount = int(update.message.text)
        context.user_data['salary_min'] = min_amount
        await update.message.reply_text(
            "Укажите максимальную сумму зарплаты (в KRW):"
        )
        return SALARY + 3  # Состояние для максимальной суммы
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите числовое значение.")
        return SALARY + 2

async def handle_salary_max(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка максимальной суммы зарплаты"""
    try:
        max_amount = int(update.message.text)
        min_amount = context.user_data['salary_min']
        if max_amount < min_amount:
            await update.message.reply_text("Максимальная сумма должна быть больше минимальной.")
            return SALARY + 3
        
        context.user_data['salary'] = f"от {min_amount:,} до {max_amount:,} KRW {context.user_data['salary_period']}"
        return await request_hashtags(update, context)
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите числовое значение.")
        return SALARY + 3

async def request_hashtags(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запрос хэштегов"""
    await update.message.reply_text(
        "Введите хэштеги через запятую:\n"
        "Например: #работа, #вакансия, #сеул"
    )
    return HASHTAGS

async def handle_hashtags(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка хэштегов"""
    hashtags = update.message.text
    # Добавляем # к тегам, если их нет
    tags = [tag.strip() if tag.strip().startswith('#') else f'#{tag.strip()}' 
            for tag in hashtags.split(',')]
    context.user_data['hashtags'] = ' '.join(tags)
    
    # Формируем предпросмотр объявления
    preview = f"{context.user_data['ad_type']}\n\n"
    preview += f"🌆 Город: {context.user_data['ad_city']}\n\n"
    preview += context.user_data['ad_content']
    preview += "\n\n💬 Вопросы задавайте в комментариях 🔽\n\n"
    
    if 'salary' in context.user_data:
        preview += f"💰 Зарплата: {context.user_data['salary']}\n\n"
    
    preview += context.user_data['hashtags']
    
    keyboard = [
        [InlineKeyboardButton("✅ Опубликовать", callback_data="publish")],
        [InlineKeyboardButton("❌ Отменить", callback_data="cancel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Если есть изображение, отправляем его с текстом
    if context.user_data.get('image_file_id'):
        await update.message.reply_photo(
            photo=context.user_data['image_file_id'],
            caption=preview,
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            preview,
            reply_markup=reply_markup
        )
    
    return CONFIRMATION

async def handle_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка подтверждения публикации"""
    query = update.callback_query
    await query.answer()
    
    try:
        if query.data == "publish":
            # Проверяем наличие всех необходимых данных
            required_fields = ['ad_type', 'ad_city', 'ad_content', 'hashtags']
            for field in required_fields:
                if field not in context.user_data:
                    await query.edit_message_text(
                        f"Ошибка: не хватает данных для публикации ({field}). "
                        "Попробуйте создать объявление заново."
                    )
                    return ConversationHandler.END
            
            # Публикуем объявление
            result = await publish_ad(update, context)
            if result:
                # Удаляем предпросмотр объявления
                await query.message.delete()
                
                # Отправляем новое сообщение об успехе
                await context.bot.send_message(
                    chat_id=query.from_user.id,
                    text="✅ Ваше объявление успешно опубликовано!"
                )
                
                # Показываем главное меню
                keyboard = [
                    ["🌟 СОЗДАТЬ ОБЪЯВЛЕНИЕ ✨", "🔍 ПОИС�� ОБЪЯВЛЕНИЙ 🎯"],
                    ["📹 ВИДЕО-ИНСТРУКЦИЯ 🎥", "👤 МОЙ ПРОФИЛЬ 💫"]
                ]
                reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
                await context.bot.send_message(
                    chat_id=query.from_user.id,
                    text="✨ Выберите действие:",
                    reply_markup=reply_markup
                )
            else:
                await query.edit_message_text(
                    "❌ Произошла ошибка при публикации объявления. "
                    "Попробуйте позже или обратитесь к администратору."
                )
        else:
            await query.message.delete()
            await context.bot.send_message(
                chat_id=query.from_user.id,
                text="❌ Публикация объявления отменена."
            )
            
            # Показываем главное меню
            keyboard = [
                ["🌟 СОЗДАТЬ ОБЪЯВЛЕНИЕ ✨", "🔍 ПОИСК ОБЪЯВЛЕНИЙ 🎯"],
                ["📹 ВИДЕО-ИНСТРУКЦИЯ 🎥", "👤 МОЙ ПРОФИЛЬ 💫"]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await context.bot.send_message(
                chat_id=query.from_user.id,
                text="✨ Выберите действие:",
                reply_markup=reply_markup
            )
        
        return ConversationHandler.END
        
    except Exception as e:
        print(f"Ошибка при обработке подтверждения: {e}")
        await query.edit_message_text(
            "Произошла ошибка. Попробуйте создать объявление заново."
        )
        return ConversationHandler.END

async def publish_ad(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Публикация объявления"""
    try:
        query = update.callback_query
        user_id = query.from_user.id
        
        # Получаем данные пользователя
        conn = sqlite3.connect('board.db')
        c = conn.cursor()
        c.execute("SELECT is_verified FROM users WHERE user_id = ?", (user_id,))
        user_data = c.fetchone()
        is_verified = user_data[0] if user_data else False
        
        # Формируем текст объявления
        ad_text = f"{context.user_data['ad_type']}\n\n"
        if is_verified:
            ad_text += "✅ Верифицированный пользователь\n\n"
        ad_text += f"🌆 Город: {context.user_data['ad_city']}\n\n"
        ad_text += context.user_data['ad_content']
        ad_text += "\n\n💬 Вопросы задавайте в комментариях 🔽\n\n"
        
        if 'salary' in context.user_data:
            ad_text += f"💰 Зарплата: {context.user_data['salary']}\n\n"
        
        ad_text += context.user_data['hashtags']
        
        # Создаем кнопку "Написать автору"
        keyboard = [[InlineKeyboardButton("✍️ Написать автору", url=f"https://t.me/{query.from_user.username}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Публикуем объявление в канал
        if context.user_data.get('image_file_id'):
            message = await context.bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=context.user_data['image_file_id'],
                caption=ad_text,
                reply_markup=reply_markup
            )
        else:
            message = await context.bot.send_message(
                chat_id=CHANNEL_ID,
                text=ad_text,
                reply_markup=reply_markup
            )
        
        # Сохраняем объявление в базу данных
        c.execute("""
            INSERT INTO ads (user_id, type, city, content, image_file_id, salary, hashtags, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'published')
        """, (
            user_id,
            context.user_data['ad_type'],
            context.user_data['ad_city'],
            context.user_data['ad_content'],
            context.user_data.get('image_file_id'),
            context.user_data.get('salary'),
            context.user_data['hashtags']
        ))
        
        # Обновляем время последней публикации и баланс
        ad_type = context.user_data['ad_type']
        if AD_TYPES[ad_type]["price"] > 0:
            c.execute("""
                UPDATE users 
                SET balance = balance - ?
                WHERE user_id = ?
            """, (AD_TYPES[ad_type]["price"], user_id))
        else:
            c.execute("""
                UPDATE users 
                SET last_free_post = CURRENT_TIMESTAMP
                WHERE user_id = ?
            """, (user_id,))
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Ошибка при публикации объявления: {e}")
        return False

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показ профиля пользователя"""
    user_id = update.effective_user.id
    
    # Получаем данные пользователя
    conn = sqlite3.connect('board.db')
    c = conn.cursor()
    c.execute("""
        SELECT city, balance, is_verified, verification_requested
        FROM users 
        WHERE user_id = ?
    """, (user_id,))
    user_data = c.fetchone()
    conn.close()
    
    if not user_data:
        await update.message.reply_text("Ошибка: профиль не найден.")
        return ConversationHandler.END
    
    city, balance, is_verified, verification_requested = user_data
    
    # Формируем текст профиля
    profile_text = f"👤 Ваш профиль:\n\n"
    profile_text += f"🌆 Город: {city}\n"
    profile_text += f"💰 Баланс: {balance:,} KRW\n"
    profile_text += f"✅ Статус: {'Верифицирован' if is_verified else 'Не верифицирован'}\n"
    
    # Создаем клавиатуру профиля
    keyboard = [
        ["🌆 Мои объявления", "🌆 Изменить город"],
        ["💎 Пополнить баланс", "💰 Перевести баланс"],
        ["🏠 Главное меню"]
    ]
    
    # Добавляем кнопку верификации, если пользователь не верифицирован
    if not is_verified and not verification_requested:
        keyboard.insert(0, ["✅ Запросить верификацию"])
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(profile_text, reply_markup=reply_markup)
    return PROFILE_MENU

async def handle_profile_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка меню профиля"""
    choice = update.message.text
    
    if choice == "🌆 Мои объявления":
        return await show_my_ads(update, context)
        
    elif choice == "🌆 Изменить город":
        # Получаем список городов
        conn = sqlite3.connect('board.db')
        c = conn.cursor()
        c.execute("SELECT name FROM cities ORDER BY name")
        cities = c.fetchall()
        conn.close()
        
        keyboard = [[city[0]] for city in cities]
        keyboard.append(["Отмена"])
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(
            "Выберите новый город:",
            reply_markup=reply_markup
        )
        return CHANGE_CITY
    
    elif choice == "💰 Пополнить баланс":
        await update.message.reply_text(
            "Введите сумму пополнения в KRW:\n"
            "Например: 50000"
        )
        return ADD_BALANCE
    
    elif choice == "💸 Перевести баланс":
        await update.message.reply_text(
            "Введите ID пользователя и сумму перевода:\n"
            "Например: 123456789 50000"
        )
        return TRANSFER_BALANCE
    
    elif choice == "✅ Запросить верификацию":
        keyboard = [
            [InlineKeyboardButton("Подтвердить", callback_data="confirm_verification")],
            [InlineKeyboardButton("Отмена", callback_data="cancel_verification")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Стоимость верификации: 50,000 KRW\n"
            "После верификации вы получите:\n"
            "✅ Отметку верификации на объявлениях\n"
            "✅ Возможность публикации платных объявлений\n"
            "✅ Снятие ограничений на частоту публикации\n\n"
            "Продолжить?",
            reply_markup=reply_markup
        )
        return VERIFICATION_CHOICE
    
    elif choice == "🏠 Главное меню":
        await show_main_menu(update, context)
        return ConversationHandler.END

    return PROFILE_MENU

async def show_my_ads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показ объявлений пользователя"""
    user_id = update.effective_user.id
    
    conn = sqlite3.connect('board.db')
    c = conn.cursor()
    c.execute("""
        SELECT id, type, city, content, status, created_at
        FROM ads 
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT 5
    """, (user_id,))
    ads = c.fetchall()
    conn.close()
    
    if not ads:
        await update.message.reply_text(
            "У вас пока нет объявлений.\n"
            "Создайте новое объявление через главное меню."
        )
        return PROFILE_MENU
    
    for ad in ads:
        ad_id, ad_type, city, content, status, created_at = ad
        text = f"📌 Объявление #{ad_id}\n"
        text += f"Тип: {ad_type}\n"
        text += f"Город: {city}\n"
        text += f"Статус: {status}\n"
        text += f"Создано: {created_at}\n\n"
        text += f"Текст: {content[:100]}..."
        
        await update.message.reply_text(text)
    
    return PROFILE_MENU

async def handle_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка пополнения баланса"""
    try:
        amount = int(update.message.text)
        if amount <= 0:
            raise ValueError
        
        # Генерируем уникальный код платежа
        payment_id = f"PAY{update.effective_user.id}_{int(datetime.now().timestamp())}"
        
        await update.message.reply_text(
            f"💳 Для пополнения баланса на {amount:,} KRW:\n\n"
            "1. Переведите указанную сумму на счет:\n"
            "KB Bank: 123-456-789\n"
            "Получатель: HONG GIL DONG\n\n"
            f"2. Укажите код платежа: {payment_id}\n\n"
            "3. После перевода отправьте скриншот чека администратору: @admin\n\n"
            "❗ Баланс будет пополнен после проверки платежа"
        )
        return PROFILE_MENU
        
    except ValueError:
        await update.message.reply_text(
            "Пожалуйста, введите корректную сумму (только цифры)."
        )
        return ADD_BALANCE

async def handle_balance_transfer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка перевода средств"""
    try:
        user_id, amount = update.message.text.split()
        target_id = int(user_id)
        amount = int(amount)
        
        if amount <= 0:
            raise ValueError
        
        # Проверяем баланс отправителя
        conn = sqlite3.connect('board.db')
        c = conn.cursor()
        
        c.execute("SELECT balance FROM users WHERE user_id = ?", (update.effective_user.id,))
        sender_balance = c.fetchone()
        
        if not sender_balance or sender_balance[0] < amount:
            await update.message.reply_text("Недостаточно средств для перевода.")
            conn.close()
            return PROFILE_MENU
        
        # Проверяем существование получателя
        c.execute("SELECT username FROM users WHERE user_id = ?", (target_id,))
        target_user = c.fetchone()
        
        if not target_user:
            await update.message.reply_text("Пользователь не найден.")
            conn.close()
            return PROFILE_MENU
        
        # Выполняем перевод
        c.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?", 
                 (amount, update.effective_user.id))
        c.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", 
                 (amount, target_id))
        
        conn.commit()
        conn.close()
        
        await update.message.reply_text(
            f"✅ Перевод {amount:,} KRW выполнен успешно!"
        )
        
    except ValueError:
        await update.message.reply_text(
            "Неверный формат. Используйте: ID_пользователя сумма\n"
            "Например: 123456789 50000"
        )
    except Exception as e:
        await update.message.reply_text("Произошла ошибка при переводе.")
        print(f"Ошибка перевода: {e}")
    
    return PROFILE_MENU

async def search_ads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Поиск объявлений"""
    keyboard = [
        ["🔍 По типу", "🌆 По городу"],
        ["#️⃣ По хэштегу", "💰 По цене"],
        ["🏠 Главное меню"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "✨ Выберите критерий поиска:",
        reply_markup=reply_markup
    )
    return SEARCH_MENU

async def handle_search_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка меню ��оиска"""
    choice = update.message.text
    
    if choice == "🔍 По типу":
        keyboard = [[type_name] for type_name in AD_TYPES.keys()]
        keyboard.append(["Отмена"])
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(
            "Выберите тип объявления:",
            reply_markup=reply_markup
        )
        return SEARCH_TYPE
    
    elif choice == "🌆 По городу":
        conn = sqlite3.connect('board.db')
        c = conn.cursor()
        c.execute("SELECT name FROM cities ORDER BY name")
        cities = c.fetchall()
        conn.close()
        
        keyboard = [[city[0]] for city in cities]
        keyboard.append(["Отмена"])
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(
            "Выберите город:",
            reply_markup=reply_markup
        )
        return SEARCH_CITY
    
    elif choice == "#️⃣ По хэштегу":
        await update.message.reply_text(
            "Введите хэштег для поиска (без #):"
        )
        return SEARCH_HASHTAG
    
    elif choice == "💰 По цене":
        await update.message.reply_text(
            "Введите диапазон цен в формате: мин макс\n"
            "Например: 2000000 3000000"
        )
        return SEARCH_PRICE
    
    elif choice == "🏠 Главное меню":
        await show_main_menu(update, context)
        return ConversationHandler.END

async def show_search_results(update: Update, context: ContextTypes.DEFAULT_TYPE, query: str, params: tuple):
    """Показ результатов поиска"""
    conn = sqlite3.connect('board.db')
    c = conn.cursor()
    
    try:
        # Выполняем запрос
        c.execute(query, params)
        ads = c.fetchall()
        
        if not ads:
            await update.message.reply_text(
                "По вашему запросу ничего не найдено."
            )
            return SEARCH_MENU
        
        for ad in ads[:5]:  # Показываем только 5 последних объявлений
            ad_text = f"{ad[2]}\n\n"  # Тип объявления
            ad_text += f"🌆 Город: {ad[3]}\n\n"  # Город
            ad_text += f"{ad[4][:200]}..."  # Текст (первые 200 символов)
            
            if ad[6]:  # Если есть зарплата
                ad_text += f"\n\n💰 Зарплата: {ad[6]}"
            
            # Получаем username автора
            c.execute("SELECT username FROM users WHERE user_id = ?", (ad[1],))
            user = c.fetchone()
            username = user[0] if user and user[0] else "tgkvork_bot"
            
            keyboard = [[InlineKeyboardButton("✍️ Написать автору", url=f"https://t.me/{username}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            if ad[5]:  # Если есть изображение
                try:
                    await update.message.reply_photo(
                        photo=ad[5],
                        caption=ad_text,
                        reply_markup=reply_markup
                    )
                except Exception as e:
                    print(f"Ошибка при отправке фото: {e}")
                    await update.message.reply_text(
                        ad_text,
                        reply_markup=reply_markup
                    )
            else:
                await update.message.reply_text(
                    ad_text,
                    reply_markup=reply_markup
                )
    
    except Exception as e:
        print(f"Ошибка при поиске: {e}")
        await update.message.reply_text(
            "Произошла ошибка при поиске. Попробуйте позже."
        )
    
    finally:
        conn.close()
    
    return SEARCH_MENU

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    print(f'Произошла ошибка: {context.error}')

# Добавьте функцию для отправки приветственного сообщения в канал
async def send_channel_greeting(context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Разместить объявление", url="https://t.me/tgkvork_bot")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text="Для размещения объявлений перейдите к боту: @tgkvork_bot\n\nили нажмите на кнопку ниже",
        reply_markup=reply_markup
    )

# Добавьте новую функцию для обработки сообщений в канале
async def handle_channel_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка сообщений в канале"""
    if update.channel_post:  # Если сообщение из канала
        # Удаляем сообщение из канала
        await context.bot.delete_message(
            chat_id=update.channel_post.chat_id,
            message_id=update.channel_post.message_id
        )
        
        # Отправляем сообщение с кнопкой
        keyboard = [[InlineKeyboardButton("Разместить объявление", url="https://t.me/tgkvork_bot")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_message(
            chat_id=update.channel_post.chat_id,
            text="Для размещения объявлений перейдите к боту: @tgkvork_bot\n\nили нажмите на кнопку ниже",
            reply_markup=reply_markup
        )

def main():
    try:
        if not BOT_TOKEN:
            raise ValueError("BOT_TOKEN не настроен в .env файле")
        if not ADMIN_ID:
            raise ValueError("ADMIN_ID не настроен в .env файле")
            
        application = Application.builder().token(BOT_TOKEN).build()
        init_db()
        
        # Добавляем обработчик ошибок
        application.add_error_handler(error_handler)
        
        # Создаем ConversationHandler
        conv_handler = ConversationHandler(
            entry_points=[
                CommandHandler("start", start),
                MessageHandler(filters.Regex("^🌟 СОЗДАТЬ ОБЪЯВЛЕНИЕ ✨$"), create_ad),
                MessageHandler(filters.Regex("^👤 МОЙ ПРОФИЛЬ 💫$"), profile),
                MessageHandler(filters.Regex("^🔍 ПОИСК ОБЪЯВЛЕНИЙ 🎯$"), search_ads),
            ],
            states={
                CONTACT: [MessageHandler(filters.CONTACT, handle_contact)],
                CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_city)],
                VERIFICATION_CHOICE: [CallbackQueryHandler(handle_verification_choice)],
                CHOOSE_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_ad_type)],
                CHOOSE_CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_city_for_ad)],
                CONTENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_content)],
                IMAGE: [
                    MessageHandler(filters.PHOTO, handle_image),
                    MessageHandler(filters.Regex("^Пропустить$"), skip_image)
                ],
                SALARY: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_salary_period)],
                SALARY + 1: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_salary_amount)],
                SALARY + 2: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_salary_min)],
                SALARY + 3: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_salary_max)],
                HASHTAGS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_hashtags)],
                CONFIRMATION: [CallbackQueryHandler(handle_confirmation)],
                PROFILE_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_profile_menu)],
                CHANGE_CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_city)],
                ADD_BALANCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_balance)],
                TRANSFER_BALANCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_balance_transfer)],
                MY_ADS: [MessageHandler(filters.TEXT & ~filters.COMMAND, show_my_ads)],
                SEARCH_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_search_menu)],
                SEARCH_TYPE: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, 
                        lambda u, c: show_search_results(u, c, 
                        "SELECT * FROM ads WHERE type = ? AND status = 'published' ORDER BY created_at DESC", 
                        (u.message.text,)))
                ],
                SEARCH_CITY: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND,
                        lambda u, c: show_search_results(u, c,
                        "SELECT * FROM ads WHERE city = ? AND status = 'published' ORDER BY created_at DESC", 
                        (u.message.text,)))
                ],
                SEARCH_HASHTAG: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND,
                        lambda u, c: show_search_results(u, c,
                        "SELECT * FROM ads WHERE hashtags LIKE ? AND status = 'published' ORDER BY created_at DESC", 
                        (f"%#{u.message.text}%",)))
                ],
                SEARCH_PRICE: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND,
                        lambda u, c: show_search_results(u, c,
                        "SELECT * FROM ads WHERE salary LIKE ? AND status = 'published' ORDER BY created_at DESC",
                        (f"%{u.message.text}%",)))
                ]
            },
            fallbacks=[CommandHandler("cancel", lambda u, c: ConversationHandler.END)]
        )
        
        # Добавляем обработчик сообщений в канале (добавьте перед conv_handler)
        application.add_handler(MessageHandler(
            filters.ChatType.CHANNEL & filters.TEXT,
            handle_channel_message
        ))
        
        application.add_handler(conv_handler)
        print("Бот запущен...")
        application.run_polling()
        
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")
        raise

if __name__ == "__main__":
    main()
