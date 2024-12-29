from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import datetime

from states.states import States
from database.db import Database
from config.settings import AD_SETTINGS, AD_CATEGORIES, ADMIN_USERNAME, CHANNEL_ID
from keyboards.keyboards import get_main_menu, get_ads_menu

db = Database('board.db')

async def show_ads_list(update: Update, ads: list, title: str):
    """Показывает список объявлений"""
    if not ads:
        await update.message.reply_text(
            f"{title}\n\n"
            "У вас пока нет объявлений в этой категории"
        )
        return States.ADS_MENU
    
    for ad in ads:
        text = (
            f"📝 *{AD_CATEGORIES[ad['type']]['icon']} {ad['content']}*\n\n"
            f"🌆 Город: {ad['city']}\n"
            f"💰 Цена: {ad['price']}\n"
            f"👁 Просмотров: {ad['views']}\n"
            f"📱 Переходов: {ad['clicks']}\n"
            f"📅 Создано: {ad['created_at']}\n"
            f"#{ad['hashtags'].replace(' ', ' #') if ad['hashtags'] else ''}"
        )
        
        await update.message.reply_text(
            text,
            parse_mode='Markdown'
        )
    
    reply_markup = get_ads_menu()
    await update.message.reply_text(
        "Выберите действие:",
        reply_markup=reply_markup
    )
    return States.ADS_MENU

async def handle_active_ads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает активные объявления"""
    ads = db.get_user_ads(update.effective_user.id, status='active')
    return await show_ads_list(update, ads, "📝 Активные объявления")

async def handle_pending_ads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает объявления на модерации"""
    ads = db.get_user_ads(update.effective_user.id, status='pending')
    return await show_ads_list(update, ads, "⏳ На модерации")

async def handle_rejected_ads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает отклоненные объявления"""
    ads = db.get_user_ads(update.effective_user.id, status='rejected')
    return await show_ads_list(update, ads, "❌ Отклоненные")

async def handle_ads_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает статистику объявлений"""
    stats = db.get_user_ads_stats(update.effective_user.id)
    
    await update.message.reply_text(
        f"📊 *Статистика объявлений*\n\n"
        f"📝 Всего: {stats['total']}\n"
        f"✅ Активных: {stats['active']}\n"
        f"⏳ На модерации: {stats['pending']}\n"
        f"❌ Отклоненных: {stats['rejected']}\n"
        f"👁 Просмотров: {stats['views']}\n"
        f"📱 Переходов: {stats['clicks']}",
        parse_mode='Markdown'
    )
    
    reply_markup = get_ads_menu()
    await update.message.reply_text(
        "Выберите действие:",
        reply_markup=reply_markup
    )
    return States.ADS_MENU

async def create_ad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало создания объявления"""
    user_id = update.effective_user.id
    
    # Проверяем возможность создания объявления
    if not db.can_post_free_ad(user_id):
        await update.message.reply_text(
            "⚠️ Вы не можете создать новое объявление сейчас.\n"
            "Подождите 3 часа после последней публикации или купите PRO-аккаунт."
        )
        return States.ADS_MENU
    
    # Показываем категории
    keyboard = []
    for category in AD_CATEGORIES:
        keyboard.append([category])
    keyboard.append(["🏠 Главное меню"])
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Выберите категорию объявления:",
        reply_markup=reply_markup
    )
    return States.AD_TYPE

async def handle_ad_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка выбора типа объявления"""
    ad_type = update.message.text
    
    if ad_type not in AD_CATEGORIES:
        await update.message.reply_text(
            "Пожалуйста, выберите категорию из списка"
        )
        return States.AD_TYPE
        
    context.user_data['ad_type'] = ad_type
    
    await update.message.reply_text(
        "Введите текст объявления:",
        reply_markup=ReplyKeyboardMarkup([["🏠 Главное меню"]], resize_keyboard=True)
    )
    return States.AD_CONTENT

async def handle_ad_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка текста объявления"""
    content = update.message.text
    
    if len(content) < AD_SETTINGS['min_length']:
        await update.message.reply_text(
            f"Минимальная длина объявления: {AD_SETTINGS['min_length']} символов"
        )
        return States.AD_CONTENT
        
    if len(content) > AD_SETTINGS['max_length']:
        await update.message.reply_text(
            f"Максимальная длина объявления: {AD_SETTINGS['max_length']} символов"
        )
        return States.AD_CONTENT
        
    context.user_data['content'] = content
    
    await update.message.reply_text(
        "Отправьте фото для объявления (или нажмите /skip для пропуска):"
    )
    return States.AD_PHOTO

async def handle_ad_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка фото объявления"""
    if update.message.photo:
        context.user_data['photo'] = update.message.photo[-1].file_id
    
    await update.message.reply_text(
        "Введите цену (или нажмите /skip для пропуска):"
    )
    return States.AD_PRICE

async def handle_ad_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка цены объявления"""
    if update.message.text != '/skip':
        # Проверяем, что цена является числом
        try:
            price = int(update.message.text.replace(',', '').replace(' ', ''))
            context.user_data['price'] = f"{price:,}"
        except ValueError:
            await update.message.reply_text(
                "❌ Пожалуйста, введите корректную цену (только цифры)\n"
                "Например: 50000 или 2500000"
            )
            return States.AD_PRICE
    
    await update.message.reply_text(
        "Введите хештеги через пробел (или нажмите /skip для пропуска):"
    )
    return States.AD_HASHTAGS

async def handle_ad_hashtags(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка хештегов и создание объявления"""
    if update.message.text != '/skip':
        hashtags = update.message.text.strip()
        if not all(tag.startswith('#') for tag in hashtags.split()):
            await update.message.reply_text(
                "❌ Неверный формат хештегов. Каждый тег должен начинаться с #\n"
                "Например: #работа #вакансия #seoul"
            )
            return States.AD_HASHTAGS
        context.user_data['hashtags'] = hashtags
    
    # Создаем объявление
    ad_id = db.create_ad(
        user_id=update.effective_user.id,
        ad_type=context.user_data['ad_type'],
        city=db.get_user(update.effective_user.id)['city'],
        content=context.user_data['content'],
        image_file_id=context.user_data.get('photo'),
        price=context.user_data.get('price'),
        hashtags=context.user_data.get('hashtags')
    )
    
    if not ad_id:
        await update.message.reply_text(
            "❌ Произошла ошибка при создании объявления. Попробуйте позже."
        )
        return States.MAIN_MENU
    
    # Отправляем на модерацию
    await send_to_moderation(context, ad_id)
    
    # Очищаем данные
    context.user_data.clear()
    
    await update.message.reply_text(
        "✅ Объявление создано и отправлено на модерацию!\n"
        "Среднее время проверки: 24 часа",
        reply_markup=get_main_menu()
    )
    return States.MAIN_MENU

async def handle_extend_ad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Продление срока действия объявления"""
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text(
            "❌ Неверный формат команды. Используйте: /extend <id объявления>"
        )
        return States.ADS_MENU
        
    ad_id = int(context.args[0])
    user_id = update.effective_user.id
    
    # Проверяем существование объявления
    ad = db.get_ad(ad_id)
    if not ad or ad['user_id'] != user_id:
        await update.message.reply_text(
            "❌ Объявление не найдено или принадлежит другому пользователю"
        )
        return States.ADS_MENU
    
    # Продлеваем объявление
    if db.extend_ad(ad_id):
        await update.message.reply_text(
            "✅ Срок действия объявления продлен на 30 дней"
        )
    else:
        await update.message.reply_text(
            "❌ Не удалось продлить объявление"
        )
    
    return States.ADS_MENU

async def send_to_moderation(context: ContextTypes.DEFAULT_TYPE, ad_id: int):
    """Отправляет объявление на модерацию"""
    ad = db.get_ad(ad_id)
    if not ad:
        return
        
    user = db.get_user(ad['user_id'])
    
    text = (
        f"📝 *Новое объявление на модерацию*\n\n"
        f"👤 Пользователь: @{user['username']}\n"
        f"📱 Контакт: {user['phone']}\n"
        f"🌆 Город: {ad['city']}\n\n"
        f"📋 *Категория:* {ad['type']}\n"
        f"💰 Цена: {ad['price'] or 'Не указана'}\n\n"
        f"*Текст объявления:*\n{ad['content']}\n\n"
        f"#{ad['hashtags'].replace(' ', ' #') if ad['hashtags'] else ''}"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("✅ Одобрить", callback_data=f"approve_{ad_id}"),
            InlineKeyboardButton("❌ Отклонить", callback_data=f"reject_{ad_id}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Отправляем админу
    try:
        await context.bot.send_message(
            chat_id=ADMIN_USERNAME,
            text=text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        
        # Если есть фото, отправляем его отдельным сообщением
        if ad['image_file_id']:
            await context.bot.send_photo(
                chat_id=ADMIN_USERNAME,
                photo=ad['image_file_id']
            )
    except Exception as e:
        print(f"Ошибка отправки на модерацию: {e}")

# ... продолжение следует ... 