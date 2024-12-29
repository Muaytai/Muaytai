from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import datetime

from states.states import States
from database.db import Database
from config.settings import ADMIN_USERNAME, PRO_PRICES
from utils.templates import Templates
from keyboards.styles import ButtonStyles

db = Database('board.db')

async def handle_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Управление балансом"""
    user = db.get_user(update.effective_user.id)
    
    # Используем шаблон для красивого отображения
    text = Templates.balance_info(user)
    
    keyboard = [
        [
            InlineKeyboardButton("💳 Пополнить", callback_data="add_balance"),
            InlineKeyboardButton("💰 Вывести", callback_data="withdraw")
        ],
        [
            InlineKeyboardButton("📊 История", callback_data="history"),
            InlineKeyboardButton("🎁 Промокод", callback_data="promo")
        ],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return States.BALANCE_MENU

async def handle_add_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Пополнение баланса"""
    keyboard = [
        [
            InlineKeyboardButton("10,000 KRW", callback_data="add_10000"),
            InlineKeyboardButton("30,000 KRW", callback_data="add_30000")
        ],
        [
            InlineKeyboardButton("50,000 KRW", callback_data="add_50000"),
            InlineKeyboardButton("100,000 KRW", callback_data="add_100000")
        ],
        [InlineKeyboardButton("💬 Другая сумма", callback_data="add_custom")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="balance")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "💳 *Пополнение баланса*\n\n"
        "Выберите сумму или введите свою:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return States.ADD_BALANCE

async def handle_payment_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка введенной суммы"""
    try:
        amount = int(update.message.text.replace(",", ""))
        if amount < 10000:
            raise ValueError("Минимальная сумма 10,000 KRW")
            
        payment_id = f"PAY{update.effective_user.id}_{int(datetime.now().timestamp())}"
        db.add_payment(payment_id, update.effective_user.id, amount)
        
        keyboard = [
            [InlineKeyboardButton("💳 Оплатить картой", callback_data=f"pay_card_{payment_id}")],
            [InlineKeyboardButton("🏦 Банковский перевод", callback_data=f"pay_bank_{payment_id}")],
            [InlineKeyboardButton("⬅️ Отмена", callback_data="balance")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"{'='*35}\n"
            f"💳 *Пополнение баланса*\n"
            f"{'='*35}\n\n"
            f"Сумма: *{amount:,} KRW*\n"
            f"ID платежа: `{payment_id}`\n\n"
            f"Выберите способ оплаты:\n"
            f"{'='*35}",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return States.PAYMENT_METHOD
        
    except ValueError as e:
        await update.message.reply_text(
            f"❌ *Ошибка*\n\n{str(e)}\n\nВведите корректную сумму",
            parse_mode='Markdown'
        )
        return States.ADD_BALANCE

async def handle_withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Вывод средств"""
    user = db.get_user(update.effective_user.id)
    
    if not user['is_verified']:
        await update.message.reply_text(
            "❌ *Вывод средств доступен только для верифицированных пользователей*\n\n"
            "Пройдите верификацию в личном кабинете",
            parse_mode='Markdown'
        )
        return States.BALANCE_MENU
    
    if user['balance'] < 50000:
        await update.message.reply_text(
            "❌ *Недостаточно средств*\n\n"
            "Минимальная сумма для вывода: 50,000 KRW",
            parse_mode='Markdown'
        )
        return States.BALANCE_MENU
    
    keyboard = [
        [InlineKeyboardButton("🏦 Банковский счет", callback_data="withdraw_bank")],
        [InlineKeyboardButton("⬅️ Отмена", callback_data="balance")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"{'='*35}\n"
        f"💰 *Вывод средств*\n"
        f"{'='*35}\n\n"
        f"Доступно: *{user['balance']:,} KRW*\n"
        f"Минимум: 50,000 KRW\n"
        f"Комиссия: 1%\n\n"
        f"Выберите способ вывода:\n"
        f"{'='*35}",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    return States.WITHDRAW_METHOD

# ... продолжение следует ... 