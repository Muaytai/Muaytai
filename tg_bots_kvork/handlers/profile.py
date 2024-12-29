from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from telegram.ext import ContextTypes
from datetime import datetime

from states.states import States
from keyboards.keyboards import get_main_menu, get_profile_menu, get_ads_menu, get_balance_menu
from database.db import Database
from utils.templates import Templates
from keyboards.styles import ButtonStyles

db = Database('board.db')

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает профиль пользователя"""
    user_id = update.effective_user.id
    user = db.get_user(user_id)
    
    if not user:
        await update.message.reply_text(
            "Профиль не найден. Используйте /start для регистрации."
        )
        return States.END
    
    city, balance, is_verified = user[3], user[4], user[5]  # city, balance, is_verified
    status = "✅ Верифицирован" if is_verified else "❌ Не верифицирован"
    
    await update.message.reply_text(
        f"👤 Ваш профиль:\n\n"
        f"🌆 Город: {city}\n"
        f"💰 Баланс: {balance:,.0f} KRW\n"
        f"✅ Статус: {status}"
    )
    
    reply_markup = get_profile_menu()
    await update.message.reply_text(
        "Выберите действие:",
        reply_markup=reply_markup
    )
    return States.PROFILE_MENU

async def handle_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает профиль пользователя"""
    user = db.get_user(update.effective_user.id)
    text = Templates.profile_info(user)
    reply_markup = InlineKeyboardMarkup(ButtonStyles.profile_buttons(user['is_verified']))
    
    await update.message.reply_text(
        text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return States.PROFILE_MENU

async def handle_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Управление балансом"""
    user = db.get_user(update.effective_user.id)
    
    await update.message.reply_text(
        f"💰 *Ваш баланс*\n\n"
        f"Доступно: {user[4]:,.0f} KRW\n"
        f"Заморожено: 0 KRW\n\n"
        f"💎 Тариф: {'PRO' if user[6] else 'Базовый'}\n"
        f"📅 Срок действия: {'Бессрочно' if user[6] else '-'}"
    )
    
    reply_markup = get_balance_menu()
    await update.message.reply_text(
        "Выберите действие:",
        reply_markup=reply_markup
    )
    return States.BALANCE_MENU

async def handle_profile_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка меню профиля"""
    text = update.message.text
    
    if text == "🏠 Главное меню":
        reply_markup = get_main_menu()
        await update.message.reply_text(
            "Выберите действие:",
            reply_markup=reply_markup
        )
        return States.END
        
    elif text == "💎 Пополнить баланс":
        await update.message.reply_text(
            "Введите сумму для пополнения (в KRW):\n"
            "Например: 50000"
        )
        return States.ADD_BALANCE
        
    else:
        await update.message.reply_text(
            "Пожалуйста, выберите действие из меню"
        )
        return States.PROFILE_MENU 

async def handle_my_ads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды 'Мои объявления'"""
    user_id = update.effective_user.id
    stats = db.get_user_ads_stats(user_id)  # Используем новый метод

    # Пример использования данных
    await update.message.reply_text(
        f"Ваши объявления:\n"
        f"Всего: {stats['total_ads']}\n"
        f"Опубликовано: {stats['published_ads']}\n"
        f"На модерации: {stats['pending_ads']}\n"
        f"Отклонено: {stats['rejected_ads']}"
    )
    return States.MAIN_MENU

async def handle_change_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка изменения города"""
    cities = db.get_cities()
    keyboard = [[city[0]] for city in cities]
    keyboard.append(["🏠 Главное меню"])
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "Выберите новый город:",
        reply_markup=reply_markup
    )
    return States.CHANGE_CITY

async def handle_transfer_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка перевода баланса"""
    await update.message.reply_text(
        "Функция в разработке"
    )
    return States.PROFILE_MENU

async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Возврат в главное меню"""
    reply_markup = get_main_menu()
    await update.message.reply_text(
        "Выберите действие:",
        reply_markup=reply_markup
    )
    return States.END 

async def handle_change_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка изменения контактных данных"""
    keyboard = [[KeyboardButton("📱 Поделиться новым контактом", request_contact=True)]]
    keyboard.append(["🏠 Главное меню"])
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "📱 *Изменение контактного номера*\n\n"
        "Для изменения номера телефона, нажмите кнопку ниже "
        "и поделитесь своим контактом.\n\n"
        "❗️ Важно: можно использовать только свой реальный номер",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return States.CHANGE_CONTACT 

async def handle_security(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Управление безопасностью аккаунта"""
    keyboard = [
        [
            InlineKeyboardButton("🔑 Сменить пароль", callback_data="change_password"),
            InlineKeyboardButton("📱 Двухфакторная аутентификация", callback_data="2fa")
        ],
        [
            InlineKeyboardButton("📋 История входов", callback_data="login_history"),
            InlineKeyboardButton("🔒 Активные сессии", callback_data="active_sessions")
        ],
        [InlineKeyboardButton("⬅️ Назад", callback_data="profile")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"{'='*35}\n"
        f"🔐 *Безопасность*\n"
        f"{'='*35}\n\n"
        f"🔑 *Текущие настройки:*\n"
        f"• Двухфакторная аутентификация: ❌\n"
        f"• Последний вход: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
        f"• Активных сессий: 1\n\n"
        f"Выберите действие:\n"
        f"{'='*35}",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return States.SECURITY_MENU 

async def handle_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает историю операций"""
    user_id = update.effective_user.id
    operations = db.get_user_operations(user_id)
    
    if not operations:
        await update.message.reply_text(
            "📋 *История операций*\n\n"
            "У вас пока нет операций",
            parse_mode='Markdown'
        )
        return States.PROFILE_MENU
    
    text = "📋 *История операций*\n\n"
    for op in operations:
        text += (
            f"{'➕' if op['type'] == 'deposit' else '➖'} "
            f"{op['amount']:,.0f} KRW - "
            f"{op['description']}\n"
            f"📅 {op['created_at'].strftime('%d.%m.%Y %H:%M')}\n\n"
        )
    
    keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data="profile")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return States.PROFILE_MENU

async def handle_payment_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает историю платежей"""
    user_id = update.effective_user.id
    payments = db.get_user_payments(user_id)
    
    if not payments:
        await update.message.reply_text(
            "💳 *История платежей*\n\n"
            "У вас пока нет платежей",
            parse_mode='Markdown'
        )
        return States.BALANCE_MENU
    
    text = "💳 *История платежей*\n\n"
    for payment in payments:
        text += (
            f"{'✅' if payment['status'] == 'completed' else '⏳'} "
            f"{payment['amount']:,.0f} KRW - "
            f"{payment['type']}\n"
            f"📅 {payment['created_at'].strftime('%d.%m.%Y %H:%M')}\n\n"
        )
    
    keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data="balance")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return States.BALANCE_MENU

async def handle_add_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка пополнения баланса"""
    await update.message.reply_text(
        "💳 *Пополнение баланса*\n\n"
        "Введите сумму для пополнения (в KRW):\n"
        "Минимальная сумма: 10,000 KRW\n"
        "Максимальная сумма: 1,000,000 KRW",
        parse_mode='Markdown'
    )
    return States.ADD_BALANCE

async def handle_withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка вывода средств"""
    user = db.get_user(update.effective_user.id)
    
    if user['balance'] < 50000:
        await update.message.reply_text(
            "❌ *Недостаточно средств*\n\n"
            "Минимальная сумма для вывода: 50,000 KRW",
            parse_mode='Markdown'
        )
        return States.BALANCE_MENU
    
    await update.message.reply_text(
        "💰 *Вывод средств*\n\n"
        "Введите сумму для вывода (в KRW):\n"
        "Минимальная сумма: 50,000 KRW\n"
        "Доступно: {:,.0f} KRW".format(user['balance']),
        parse_mode='Markdown'
    )
    return States.WITHDRAW

async def handle_promo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка промокода"""
    await update.message.reply_text(
        "🎁 *Активация промокода*\n\n"
        "Введите промокод:",
        parse_mode='Markdown'
    )
    return States.PROMO_CODE 

async def handle_buy_pro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Покупка PRO-аккаунта"""
    keyboard = [
        [InlineKeyboardButton(f"1 месяц - {PRO_PRICES['1_month']:,} KRW", callback_data="pro_1_month")],
        [InlineKeyboardButton(f"3 месяца - {PRO_PRICES['3_months']:,} KRW", callback_data="pro_3_months")],
        [InlineKeyboardButton(f"6 месяцев - {PRO_PRICES['6_months']:,} KRW", callback_data="pro_6_months")],
        [InlineKeyboardButton(f"12 месяцев - {PRO_PRICES['12_months']:,} KRW", callback_data="pro_12_months")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="balance")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "💎 *Тарифы PRO-аккаунта*\n\n"
        "• Неограниченное количество объявлений\n"
        "• Приоритет в поиске\n"
        "• Выделение цветом\n"
        "• Расширенная статистика\n\n"
        "Выберите период:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return States.PRO_MENU 

async def handle_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка выбранного города"""
    city = update.message.text
    
    # Сохраняем пользователя
    user_id = update.effective_user.id
    username = update.effective_user.username or "user"
    phone = context.user_data.get('phone')
    
    db.add_user(user_id, username, phone, city)
    
    # Показываем главное меню
    reply_markup = get_main_menu()
    await update.message.reply_text(
        "✅ Регистрация завершена! Выберите действие:",
        reply_markup=reply_markup
    )
    return ConversationHandler.END 