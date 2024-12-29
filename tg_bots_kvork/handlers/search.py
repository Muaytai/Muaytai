from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from states.states import States
from database.db import Database
from utils.templates import Templates
from keyboards.styles import ButtonStyles

db = Database('board.db')

async def handle_search_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает меню поиска"""
    keyboard = [
        [
            InlineKeyboardButton("🔍 По категории", callback_data="search_category"),
            InlineKeyboardButton("🌆 По городу", callback_data="search_city")
        ],
        [
            InlineKeyboardButton("💰 По цене", callback_data="search_price"),
            InlineKeyboardButton("🔍 По тексту", callback_data="search_text")
        ],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"{'='*35}\n"
        f"🔍 *Поиск объявлений*\n"
        f"{'='*35}\n\n"
        f"Выберите параметр поиска:\n"
        f"• По категории\n"
        f"• По городу\n"
        f"• По цене\n"
        f"• По тексту\n"
        f"{'='*35}",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return States.SEARCH_MENU

async def show_search_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает результаты поиска"""
    query = update.callback_query
    await query.answer()
    
    search_type = query.data.split('_')[1]
    ads = db.search_ads(search_type, context.user_data.get('search_query', ''))
    
    if not ads:
        await query.message.edit_text(
            "😕 По вашему запросу ничего не найдено\n\n"
            "Попробуйте изменить параметры поиска",
            reply_markup=ButtonStyles.search_menu_buttons()
        )
        return States.SEARCH_MENU
    
    # Показываем результаты
    for ad in ads:
        user = db.get_user(ad['user_id'])
        text = Templates.ad_card(ad, user)
        await query.message.reply_text(text, parse_mode='Markdown')
    
    return States.SEARCH_MENU 