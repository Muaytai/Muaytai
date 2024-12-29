from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import datetime

from states.states import States
from database.db import Database
from config.settings import ADMIN_USERNAME, CHANNEL_ID
from utils.templates import Templates

db = Database('board.db')

async def admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает админ-меню"""
    if update.effective_user.username != ADMIN_USERNAME:
        return
        
    keyboard = [
        [
            InlineKeyboardButton("📝 Модерация", callback_data="mod_ads"),
            InlineKeyboardButton("✅ Верификация", callback_data="mod_verify")
        ],
        [
            InlineKeyboardButton("👥 Пользователи", callback_data="mod_users"),
            InlineKeyboardButton("💰 Финансы", callback_data="mod_finance")
        ],
        [
            InlineKeyboardButton("📊 Статистика", callback_data="mod_stats"),
            InlineKeyboardButton("⚙️ Настройки", callback_data="mod_settings")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"{'='*35}\n"
        f"👨‍💼 *Панель администратора*\n"
        f"{'='*35}\n\n"
        f"*Доступные разделы:*\n"
        f"• Модерация объявлений\n"
        f"• Верификация пользователей\n"
        f"• Управление пользователями\n"
        f"• Финансовые операции\n"
        f"• Статистика и аналитика\n"
        f"• Системные настройки\n"
        f"{'='*35}",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return States.ADMIN_MENU

async def moderate_ads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает объявления на модерацию"""
    query = update.callback_query
    await query.answer()
    
    # Получаем объявления на модерации
    ads = db.get_pending_ads()
    if not ads:
        await query.message.edit_text(
            f"{'='*35}\n"
            f"✅ *Модерация объявлений*\n"
            f"{'='*35}\n\n"
            f"Нет объявлений на модерации\n"
            f"{'='*35}",
            parse_mode='Markdown'
        )
        return States.ADMIN_MENU
        
    # Показываем первое объявление
    ad = ads[0]
    context.user_data['current_ad'] = ad
    
    user = db.get_user(ad['user_id'])
    text = Templates.ad_card(ad, user)
    
    keyboard = [
        [
            InlineKeyboardButton("✅ Одобрить", callback_data=f"approve_ad_{ad['id']}"),
            InlineKeyboardButton("❌ Отклонить", callback_data=f"reject_ad_{ad['id']}")
        ],
        [InlineKeyboardButton("⬅️ Назад", callback_data="admin_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if ad['image_file_id']:
        await query.message.reply_photo(
            photo=ad['image_file_id'],
            caption=text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    else:
        await query.message.edit_text(
            text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    return States.ADMIN_MODERATE

async def approve_ad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Одобряет объявление"""
    query = update.callback_query
    await query.answer()
    
    ad_id = int(query.data.split('_')[2])
    ad = db.get_ad(ad_id)
    
    # Публикуем в канал
    text = Templates.ad_card(ad, db.get_user(ad['user_id']))
    
    if ad['image_file_id']:
        message = await context.bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=ad['image_file_id'],
            caption=text,
            parse_mode='Markdown'
        )
    else:
        message = await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=text,
            parse_mode='Markdown'
        )
    
    # Обновляем статус
    db.approve_ad(ad_id, message.message_id)
    
    # Уведомляем пользователя
    await context.bot.send_message(
        chat_id=ad['user_id'],
        text=f"{'='*35}\n"
             f"✅ *Объявление одобрено*\n"
             f"{'='*35}\n\n"
             f"Ваше объявление успешно прошло модерацию\n"
             f"и опубликовано в канале!\n"
             f"{'='*35}",
        parse_mode='Markdown'
    )
    
    await moderate_ads(update, context)

async def reject_ad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отклоняет объявление"""
    query = update.callback_query
    await query.answer()
    
    ad_id = int(query.data.split('_')[2])
    context.user_data['reject_ad_id'] = ad_id
    
    keyboard = [
        [InlineKeyboardButton("📝 Своя причина", callback_data="reject_custom")],
        [
            InlineKeyboardButton("🚫 Спам", callback_data="reject_spam"),
            InlineKeyboardButton("🔞 18+", callback_data="reject_18plus")
        ],
        [
            InlineKeyboardButton("📄 Формат", callback_data="reject_format"),
            InlineKeyboardButton("💰 Цена", callback_data="reject_price")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.edit_text(
        f"{'='*35}\n"
        f"❌ *Отклонение объявления*\n"
        f"{'='*35}\n\n"
        f"Выберите причину отклонения:\n"
        f"{'='*35}",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return States.ADMIN_REJECT_REASON

async def handle_reject_reason(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка причины отклонения"""
    query = update.callback_query
    await query.answer()
    
    reason = {
        'reject_spam': 'Спам/реклама запрещенных товаров',
        'reject_18plus': 'Контент 18+',
        'reject_format': 'Неверный формат объявления',
        'reject_price': 'Некорректная цена',
        'reject_custom': None
    }.get(query.data)
    
    if reason is None:
        await query.message.edit_text(
            f"{'='*35}\n"
            f"📝 *Укажите причину отклонения*\n"
            f"{'='*35}\n\n"
            f"Напишите причину отклонения\n"
            f"объявления одним сообщением\n"
            f"{'='*35}",
            parse_mode='Markdown'
        )
        return States.ADMIN_CUSTOM_REASON
    
    ad_id = context.user_data['reject_ad_id']
    db.reject_ad(ad_id, reason)
    
    # Уведомляем пользователя
    ad = db.get_ad(ad_id)
    await context.bot.send_message(
        chat_id=ad['user_id'],
        text=f"{'='*35}\n"
             f"❌ *Объявление отклонено*\n"
             f"{'='*35}\n\n"
             f"Причина: {reason}\n\n"
             f"Вы можете исправить замечания\n"
             f"и подать объявление повторно\n"
             f"{'='*35}",
        parse_mode='Markdown'
    )
    
    await moderate_ads(update, context)

async def handle_verification(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Управление верификацией пользователей"""
    query = update.callback_query
    await query.answer()
    
    # Получаем заявки на верификацию
    requests = db.get_pending_verifications()
    if not requests:
        await query.message.edit_text(
            f"{'='*35}\n"
            f"✅ *Верификация пользователей*\n"
            f"{'='*35}\n\n"
            f"Нет заявок на верификацию\n"
            f"{'='*35}",
            parse_mode='Markdown'
        )
        return States.ADMIN_MENU
    
    # Показываем первую заявку
    req = requests[0]
    context.user_data['current_verification'] = req
    
    keyboard = [
        [
            InlineKeyboardButton("✅ Подтвердить", callback_data=f"verify_approve_{req['verification_id']}"),
            InlineKeyboardButton("❌ Отклонить", callback_data=f"verify_reject_{req['verification_id']}")
        ],
        [InlineKeyboardButton("⬅️ Назад", callback_data="admin_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Отправляем фото документа
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=req['document_photo'],
        caption=f"{'='*35}\n"
                f"📄 *Документ*\n"
                f"{'='*35}",
        parse_mode='Markdown'
    )
    
    # Отправляем селфи
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=req['selfie_photo'],
        caption=f"{'='*35}\n"
                f"🤳 *Селфи с документом*\n"
                f"{'='*35}\n\n"
                f"👤 Пользователь: {req['username']}\n"
                f"📱 Телефон: {req['phone']}\n"
                f"📍 Адрес: {req['address']}\n"
                f"{'='*35}",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return States.ADMIN_VERIFY

async def handle_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Управление пользователями"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("🔍 Поиск", callback_data="users_search"),
            InlineKeyboardButton("📊 Статистика", callback_data="users_stats")
        ],
        [
            InlineKeyboardButton("🚫 Бан-лист", callback_data="users_banned"),
            InlineKeyboardButton("💎 PRO", callback_data="users_pro")
        ],
        [InlineKeyboardButton("⬅️ Назад", callback_data="admin_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    stats = db.get_users_stats()
    
    await query.message.edit_text(
        f"{'='*35}\n"
        f"👥 *Управление пользователями*\n"
        f"{'='*35}\n\n"
        f"📊 *Статистика:*\n"
        f"• Всего: {stats['total']}\n"
        f"• Активных: {stats['active']}\n"
        f"• Верифицировано: {stats['verified']}\n"
        f"• PRO: {stats['pro']}\n"
        f"• Заблокировано: {stats['banned']}\n\n"
        f"Выберите действие:\n"
        f"{'='*35}",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return States.ADMIN_USERS

async def handle_finance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Управление финансами"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("💳 Платежи", callback_data="finance_payments"),
            InlineKeyboardButton("💰 Выводы", callback_data="finance_withdrawals")
        ],
        [
            InlineKeyboardButton("🎁 Промокоды", callback_data="finance_promos"),
            InlineKeyboardButton("📊 Отчеты", callback_data="finance_reports")
        ],
        [InlineKeyboardButton("⬅️ Назад", callback_data="admin_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    stats = db.get_finance_stats()
    
    await query.message.edit_text(
        f"{'='*35}\n"
        f"💰 *Управление финансами*\n"
        f"{'='*35}\n\n"
        f"📊 *Статистика за сегодня:*\n"
        f"• Платежей: {stats['payments_count']}\n"
        f"• На сумму: {stats['payments_sum']:,} KRW\n"
        f"• Выводов: {stats['withdrawals_count']}\n"
        f"• На сумму: {stats['withdrawals_sum']:,} KRW\n\n"
        f"💎 *PRO-аккаунты:*\n"
        f"• Активаций: {stats['pro_activations']}\n"
        f"• Доход: {stats['pro_income']:,} KRW\n\n"
        f"Выберите раздел:\n"
        f"{'='*35}",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return States.ADMIN_FINANCE

async def handle_moderation_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка кнопок модерации"""
    query = update.callback_query
    await query.answer()
    
    action, ad_id = query.data.split('_')
    ad_id = int(ad_id)
    
    ad = db.get_ad(ad_id)
    if not ad:
        await query.edit_message_text("Объявление не найдено")
        return
    
    user_id = ad['user_id']
    
    if action == 'approve':
        db.update_ad_status(ad_id, 'published')
        await query.edit_message_text(
            f"{query.message.text}\n\n✅ Одобрено"
        )
        # Уведомляем пользователя
        await context.bot.send_message(
            chat_id=user_id,
            text="✅ Ваше объявление одобрено и опубликовано!"
        )
        
    elif action == 'reject':
        db.update_ad_status(ad_id, 'rejected')
        await query.edit_message_text(
            f"{query.message.text}\n\n❌ Отклонено"
        )
        # Уведомляем пользователя
        await context.bot.send_message(
            chat_id=user_id,
            text="❌ Ваше объявление отклонено модератором."
        )

# ... продолжение следует ... 