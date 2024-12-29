import asyncio
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    filters, ConversationHandler, CallbackQueryHandler, ContextTypes
)
import os

from config.settings import BOT_TOKEN, ADMIN_USERNAME, CHANNEL_ID
from database.db import Database
from states.states import States
from keyboards.keyboards import get_main_menu
from handlers.ads import (
    create_ad, handle_ad_type, handle_active_ads, 
    handle_pending_ads, handle_rejected_ads, 
    handle_ads_stats, handle_ad_content, handle_ad_photo,
    handle_ad_price, handle_ad_hashtags
)
from handlers.profile import (
    handle_profile, handle_balance, handle_profile_menu,
    handle_my_ads, handle_change_city, handle_transfer_balance, 
    handle_main_menu, handle_change_contact, handle_security,
    handle_history, handle_payment_history, handle_add_balance,
    handle_withdraw, handle_promo, handle_buy_pro
)
from handlers.search import handle_search_menu, show_search_results
from handlers.rules import show_rules
from handlers.help import (
    show_help, show_rules, show_faq,
    show_contacts, handle_support,
    handle_support_message
)
from handlers.verification import handle_verification
from handlers.admin import handle_moderation_callback

# Инициализация базы данных
db_file = 'board.db'
db = Database(db_file)

# Создаем структуру базы данных при первом запуске
if not os.path.exists(db_file):
    db.init_db()
    # Создаем тестовые данные только при первом запуске
    from tests.test_data import create_test_data
    create_test_data()
else:
    # Проверяем существование таблиц и создаем их при необходимости
    db.init_db()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало работы с ботом"""
    if update.effective_chat.type != 'private':
        await update.message.reply_text(
            "Пожалуйста, начните диалог со мной в личных сообщениях:\n"
            "@tgkvork_bot"
        )
        return ConversationHandler.END
        
    user_id = update.effective_user.id
    user = db.get_user(user_id)
    
    if user:
        # Если пользователь уже зарегистрирован и пришел по кнопке "Разместить объявление"
        if context.args and context.args[0] == "post":
            return await create_ad(update, context)
        # Иначе показываем главное меню
        reply_markup = get_main_menu()
        await update.message.reply_text(
            "Выберите действие:",
            reply_markup=reply_markup
        )
        return States.MAIN_MENU
    
    # Для новых пользователей начинаем регистрацию
    keyboard = [[KeyboardButton("Поделиться контактом", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Для регистрации поделитесь своим контактом",
        reply_markup=reply_markup
    )
    return States.CONTACT

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка полученного контакта"""
    contact = update.message.contact
    if contact.user_id != update.effective_user.id:
        await update.message.reply_text("Пожалуйста, отправьте свой контакт.")
        return States.CONTACT
    
    context.user_data['phone'] = contact.phone_number
    
    reply_markup = ReplyKeyboardMarkup([["🏠 Главное меню"]], resize_keyboard=True)
    await update.message.reply_text(
        "Введите название вашего города:",
        reply_markup=reply_markup
    )
    return States.CITY

async def handle_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка выбранного города"""
    city = update.message.text
    
    if not db.city_exists(city):
        await update.message.reply_text("Пожалуйста, выберите город из списка.")
        return States.CITY
    
    # Сохраняем пользователя
    user_id = update.effective_user.id
    username = update.effective_user.username or "user"
    phone = context.user_data.get('phone')
    
    db.add_user(user_id, username, phone, city)
    
    # Показываем главное меню
    reply_markup = get_main_menu()
    await update.message.reply_text(
        "Регистрация завершена! Выберите действие:",
        reply_markup=reply_markup
    )
    return ConversationHandler.END

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ошибок"""
    print(f'Произошла ошибка: {context.error}')
    if update:
        print(f'Update: {update}')
    if context:
        print(f'Context: {context}')

async def handle_channel_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка сообщений в канале"""
    if update.channel_post:  # Если сообщение из канала
        # Удаляем исходное сообщение
        await context.bot.delete_message(
            chat_id=update.channel_post.chat_id,
            message_id=update.channel_post.message_id
        )
        
        # Отправляем сообщение с кнопкой
        keyboard = [[InlineKeyboardButton(
            "Разместить объявление", 
            url=f"https://t.me/{context.bot.username}?start=post"
        )]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_message(
            chat_id=update.channel_post.chat_id,
            text="Для размещения объявлений перейдите к боту: @tgkvork_bot\n\nили нажмите на кнопку ниже",
            reply_markup=reply_markup
        )

async def handle_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отмена текущей операции"""
    reply_markup = get_main_menu()
    await update.message.reply_text(
        "Операция отменена. Выберите действие:",
        reply_markup=reply_markup
    )
    return ConversationHandler.END

async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Возврат в главное меню"""
    reply_markup = get_main_menu()
    await update.message.reply_text(
        "Выберите действие:",
        reply_markup=reply_markup
    )
    return States.MAIN_MENU

def main():
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Добавляем обработчик сообщений в канале
        application.add_handler(MessageHandler(
            filters.ChatType.CHANNEL & filters.TEXT, 
            handle_channel_message
        ))
        
        # Добавляем обработчик для модерации
        application.add_handler(CallbackQueryHandler(
            handle_moderation_callback,
            pattern=r"^(approve|reject)_\d+$"
        ))

        # Создаем ConversationHandler
        conv_handler = ConversationHandler(
            entry_points=[
                CommandHandler("start", start),
                MessageHandler(filters.Regex("^📝 Подать объявление$"), create_ad),
                MessageHandler(filters.Regex("^👤 Личный кабинет$"), handle_profile),
                MessageHandler(filters.Regex("^📊 Мои объявления$"), handle_my_ads),
                MessageHandler(filters.Regex("^ℹ️ Помощь$"), show_help),
                MessageHandler(filters.Regex("^💰 Баланс$"), handle_balance),
            ],
            states={
                States.MAIN_MENU: [
                    MessageHandler(filters.Regex("^📝 Подать объявление$"), create_ad),
                    MessageHandler(filters.Regex("^👤 Личный кабинет$"), handle_profile),
                    MessageHandler(filters.Regex("^📊 Мои объявления$"), handle_my_ads),
                    MessageHandler(filters.Regex("^🔍 Поиск объявлений$"), handle_search_menu),
                    MessageHandler(filters.Regex("^ℹ️ Помощь$"), show_help),
                    MessageHandler(filters.Regex("^💰 Баланс$"), handle_balance),
                ],
                States.CONTACT: [
                    MessageHandler(filters.CONTACT, handle_contact)
                ],
                States.CITY: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_city)
                ],
                States.PROFILE_MENU: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_profile_menu)
                ],
                States.BALANCE_MENU: [
                    MessageHandler(filters.Regex("^💳 Пополнить баланс$"), handle_add_balance),
                    MessageHandler(filters.Regex("^📊 История платежей$"), handle_payment_history),
                    MessageHandler(filters.Regex("^💎 Купить PRO$"), handle_buy_pro),
                    MessageHandler(filters.Regex("^💰 Вывод средств$"), handle_withdraw),
                    MessageHandler(filters.Regex("^🎁 Промокод$"), handle_promo),
                ],
                States.ADS_MENU: [
                    MessageHandler(filters.Regex("^📝 Активные$"), handle_active_ads),
                    MessageHandler(filters.Regex("^⏳ На модерации$"), handle_pending_ads),
                    MessageHandler(filters.Regex("^❌ Отклоненные$"), handle_rejected_ads),
                    MessageHandler(filters.Regex("^📊 Статистика$"), handle_ads_stats),
                ],
                States.AD_TYPE: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_ad_type)
                ],
                States.AD_CONTENT: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_ad_content)
                ],
                States.AD_PHOTO: [
                    MessageHandler(filters.PHOTO, handle_ad_photo),
                    MessageHandler(filters.Regex("^/skip$"), handle_ad_photo)
                ],
                States.AD_PRICE: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_ad_price),
                    MessageHandler(filters.Regex("^/skip$"), handle_ad_price)
                ],
                States.AD_HASHTAGS: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_ad_hashtags),
                    MessageHandler(filters.Regex("^/skip$"), handle_ad_hashtags)
                ],
            },
            fallbacks=[
                CommandHandler("cancel", handle_cancel),
                MessageHandler(filters.Regex("^🏠 Главное меню$"), handle_main_menu)
            ]
        )
        
        application.add_handler(conv_handler)
        
        print("Бот запущен...")
        application.run_polling()
        
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")
        raise

if __name__ == "__main__":
    main()
