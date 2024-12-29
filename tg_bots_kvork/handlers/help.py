from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from states.states import States
from keyboards.keyboards import get_help_menu, get_main_menu

async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает меню помощи"""
    reply_markup = get_help_menu()
    await update.message.reply_text(
        "ℹ️ Выберите раздел помощи:",
        reply_markup=reply_markup
    )
    return States.HELP_MENU

async def show_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает правила размещения объявлений"""
    rules_text = (
        "📜 *ПРАВИЛА РАЗМЕЩЕНИЯ ОБЪЯВЛЕНИЙ:*\n\n"
        "1️⃣ Запрещены:\n"
        "• Спам и реклама сторонних ресурсов\n"
        "• Нецензурная лексика\n"
        "• Мошеннические схемы\n\n"
        "2️⃣ Требования к объявлениям:\n"
        "• Четкое описание\n"
        "• Актуальная информация\n"
        "• Корректные контактные данные\n\n"
        "3️⃣ Ограничения:\n"
        "• Бесплатные объявления - раз в 3 часа\n"
        "• Платные объявления - без ограничений\n\n"
        "❗️ Нарушение правил ведет к блокировке"
    )
    await update.message.reply_text(rules_text, parse_mode='Markdown')
    return States.HELP_MENU

async def show_faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает часто задаваемые вопросы"""
    faq_text = (
        "❓ *ЧАСТО ЗАДАВАЕМЫЕ ВОПРОСЫ:*\n\n"
        "*Как подать объявление?*\n"
        "Нажмите кнопку 'Подать объявление' и следуйте инструкциям\n\n"
        "*Как продлить объявление?*\n"
        "В разделе 'Мои объявления' выберите нужное и нажмите 'Продлить'\n\n"
        "*Как стать PRO пользователем?*\n"
        "В разделе 'Баланс' выберите 'Купить PRO'\n\n"
        "*Как пройти верификацию?*\n"
        "В личном кабинете нажмите 'Верификация' и следуйте инструкциям"
    )
    await update.message.reply_text(faq_text, parse_mode='Markdown')
    return States.HELP_MENU

async def show_contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает контактную информацию"""
    contacts_text = (
        "📱 *НАШИ КОНТАКТЫ:*\n\n"
        "📧 Email: support@kvork.com\n"
        "💬 Telegram: @kvork_support\n"
        "🌐 Сайт: kvork.com\n\n"
        "⏰ Время работы поддержки:\n"
        "Пн-Пт: 9:00 - 18:00 (KST)"
    )
    await update.message.reply_text(contacts_text, parse_mode='Markdown')
    return States.HELP_MENU

async def handle_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка обращения в поддержку"""
    await update.message.reply_text(
        "💬 Напишите ваше сообщение для службы поддержки:",
        reply_markup=ReplyKeyboardMarkup([["🏠 Главное меню"]], resize_keyboard=True)
    )
    return States.SUPPORT_MESSAGE

async def handle_support_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка сообщения для поддержки"""
    # Здесь можно добавить логику сохранения обращения в базу данных
    await update.message.reply_text(
        "✅ Ваше сообщение отправлено! Мы ответим в течение 24 часов.",
        reply_markup=get_main_menu()
    )
    return States.MAIN_MENU 