from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton

def get_main_menu():
    keyboard = [
        ["📝 Подать объявление", "🔍 Поиск объявлений"],
        ["👤 Личный кабинет", "📊 Мои объявления"],
        ["ℹ️ Помощь", "💰 Баланс"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_profile_menu():
    keyboard = [
        ["✅ Верификация", "🌆 Изменить город"],
        ["📱 Изменить контакт", "🔐 Безопасность"],
        ["📋 История операций", "🏠 Главное меню"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_ads_menu() -> ReplyKeyboardMarkup:
    """Возвращает клавиатуру для меню объявлений"""
    keyboard = [
        ["📝 Активные", "⏳ На модерации"],
        ["❌ Отклоненные", "📊 Статистика"],
        ["📝 Подать объявление"],
        ["🏠 Главное меню"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_balance_menu():
    keyboard = [
        ["💳 Пополнить баланс", "📊 История платежей"],
        ["💎 Купить PRO", "💰 Вывод средств"],
        ["🎁 Промокод", "🏠 Главное меню"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_help_menu() -> ReplyKeyboardMarkup:
    """Возвращает клавиатуру для меню помощи"""
    keyboard = [
        ["📖 Правила размещения", "❓ Частые вопросы"],
        ["💬 Написать в поддержку", "📱 Наши контакты"],
        ["🏠 Главное меню"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True) 