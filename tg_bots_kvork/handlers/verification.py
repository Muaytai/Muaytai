from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import datetime

from states.states import States
from keyboards.keyboards import get_main_menu, get_profile_menu
from database.db import Database
from config.settings import ADMIN_USERNAME

db = Database('board.db')

async def handle_verification(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало процесса верификации"""
    user = db.get_user(update.effective_user.id)
    
    if user['is_verified']:
        await update.message.reply_text(
            "✅ Ваш аккаунт уже верифицирован!"
        )
        return States.PROFILE_MENU
        
    if user['verification_requested']:
        await update.message.reply_text(
            "⏳ Ваша заявка на верификацию находится на рассмотрении\n"
            "Среднее время проверки: 24 часа"
        )
        return States.PROFILE_MENU
    
    await update.message.reply_text(
        "📝 *Верификация аккаунта*\n\n"
        "Для верификации необходимо:\n"
        "1️⃣ Загрузить фото ID-карты/паспорта\n"
        "2️⃣ Сделать селфи с документом\n"
        "3️⃣ Указать адрес проживания\n\n"
        "Преимущества верификации:\n"
        "✅ Неограниченное количество объявлений\n"
        "✅ Приоритет в поиске\n"
        "✅ Специальный значок верификации\n"
        "✅ Доступ к PRO-функциям\n\n"
        "Отправьте фото ID-карты/паспорта:",
        parse_mode='Markdown'
    )
    return States.VERIFICATION_DOCUMENT

async def handle_document_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка фото документа"""
    if not update.message.photo:
        await update.message.reply_text(
            "❌ Пожалуйста, отправьте фото документа"
        )
        return States.VERIFICATION_DOCUMENT
    
    # Сохраняем file_id фото документа
    context.user_data['document_photo'] = update.message.photo[-1].file_id
    
    await update.message.reply_text(
        "✅ Фото документа получено\n\n"
        "Теперь сделайте селфи, держа документ рядом с лицом"
    )
    return States.VERIFICATION_SELFIE

async def handle_selfie_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка селфи с документом"""
    if not update.message.photo:
        await update.message.reply_text(
            "❌ Пожалуйста, отправьте селфи с документом"
        )
        return States.VERIFICATION_SELFIE
    
    # Сохраняем file_id селфи
    context.user_data['selfie_photo'] = update.message.photo[-1].file_id
    
    await update.message.reply_text(
        "✅ Селфи получено\n\n"
        "Укажите ваш адрес проживания:"
    )
    return States.VERIFICATION_ADDRESS

async def handle_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка адреса"""
    address = update.message.text
    
    if len(address) < 10:
        await update.message.reply_text(
            "❌ Пожалуйста, укажите полный адрес"
        )
        return States.VERIFICATION_ADDRESS
    
    # Создаем заявку на верификацию
    verification_id = db.create_verification_request(
        user_id=update.effective_user.id,
        document_photo=context.user_data['document_photo'],
        selfie_photo=context.user_data['selfie_photo'],
        address=address
    )
    
    # Отправляем данные админу
    await context.bot.send_message(
        chat_id=ADMIN_USERNAME,
        text=f"📝 *Новая заявка на верификацию*\n"
        f"🆔 Заявка: `{verification_id}`\n"
        f"👤 Пользователь: {update.effective_user.username}\n"
        f"📍 Адрес: {address}",
        parse_mode='Markdown'
    )
    
    # Отправляем фотографии
    await context.bot.send_photo(
        chat_id=ADMIN_USERNAME,
        photo=context.user_data['document_photo'],
        caption="📄 Документ"
    )
    await context.bot.send_photo(
        chat_id=ADMIN_USERNAME,
        photo=context.user_data['selfie_photo'],
        caption="🤳 Селфи с документом"
    )
    
    # Очищаем данные
    context.user_data.clear()
    
    await update.message.reply_text(
        "✅ Заявка на верификацию отправлена!\n\n"
        "Среднее время проверки: 24 часа\n"
        "Результат придет в личные сообщения",
        reply_markup=get_profile_menu()
    )
    return States.PROFILE_MENU 