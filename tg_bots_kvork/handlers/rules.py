from telegram import Update
from telegram.ext import ContextTypes

from states.states import States
from keyboards.keyboards import get_main_menu

async def show_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает правила размещения объявлений"""
    rules_text = (
        "📜 ПРАВИЛА РАЗМЕЩЕНИЯ ОБЪЯВЛЕНИЙ:\n\n"
        "1️⃣ Запрещены:\n"
        "   • Спам и реклама сторонних ресурсов\n"
        "   • Нецензурная лексика\n"
        "   • Мошеннические схемы\n\n"
        "2️⃣ Требования к объявлениям:\n"
        "   • Четкое описание\n"
        "   • Актуальная информация\n"
        "   • Корректные контактные данные\n\n"
        "3️⃣ Ограничения:\n"
        "   • Бесплатные объявления - раз в 3 часа\n"
        "   • Платные объявления - без ограничений\n\n"
        "❗️ Нарушение правил ведет к блокировке"
    )
    
    await update.message.reply_text(rules_text)
    
    reply_markup = get_main_menu()
    await update.message.reply_text(
        "Выберите действие:",
        reply_markup=reply_markup
    )
    return States.END 