from typing import Dict, Any

class Templates:
    """Шаблоны сообщений с красивым форматированием"""
    
    @staticmethod
    def profile_info(user: Dict[str, Any]) -> str:
        status = "✅ Верифицирован" if user['is_verified'] else "❌ Не верифицирован"
        pro_badge = "💎 PRO" if user['is_pro'] else "👤 Базовый"
        
        return (
            f"{'='*35}\n"
            f"👤 *Личный кабинет* {pro_badge}\n"
            f"{'='*35}\n\n"
            f"🆔 ID: `{user['user_id']}`\n"
            f"👤 Имя: {user['username']}\n"
            f"📱 Телефон: `{user['phone']}`\n"
            f"🌆 Город: {user['city']}\n\n"
            f"💰 Баланс: *{user['balance']:,} KRW*\n"
            f"✨ Статус: {status}\n"
            f"📅 С нами с: {user['registration_date'].split()[0]}\n"
            f"{'='*35}"
        )

    @staticmethod
    def ad_card(ad: Dict[str, Any], user: Dict[str, Any]) -> str:
        status_emoji = {
            'pending': '⏳',
            'published': '✅',
            'rejected': '❌',
            'expired': '⌛️'
        }
        
        return (
            f"{'='*35}\n"
            f"📝 *Объявление #{ad['id']}* {status_emoji.get(ad['status'], '')}\n"
            f"{'='*35}\n\n"
            f"👤 Автор: {user['username']}\n"
            f"📱 Телефон: `{user['phone']}`\n"
            f"🌆 Город: {ad['city']}\n"
            f"📂 Категория: {ad['type']}\n\n"
            f"💬 *Описание:*\n{ad['content']}\n\n"
            f"💰 Цена: *{ad['price'] or 'Не указана'}*\n"
            f"🏷 Теги: {ad['hashtags'] or 'Нет'}\n"
            f"{'='*35}"
        )

    @staticmethod
    def stats_card(stats: Dict[str, Any]) -> str:
        return (
            f"{'='*35}\n"
            f"📊 *Статистика объявлений*\n"
            f"{'='*35}\n\n"
            f"📝 Активные: *{stats['active']}*\n"
            f"⏳ На модерации: *{stats['pending']}*\n"
            f"❌ Отклоненные: *{stats['rejected']}*\n\n"
            f"👁 Просмотры: *{stats['views']:,}*\n"
            f"🔍 Переходы: *{stats['clicks']:,}*\n"
            f"{'='*35}"
        )

    @staticmethod
    def help_menu() -> str:
        return (
            f"{'='*35}\n"
            f"ℹ️ *Помощь и поддержка*\n"
            f"{'='*35}\n\n"
            f"📝 *Разделы:*\n\n"
            f"📖 Правила размещения\n"
            f"❓ Частые вопросы\n"
            f"💬 Написать в поддержку\n"
            f"📱 Наши контакты\n\n"
            f"🔍 Выберите интересующий раздел\n"
            f"{'='*35}"
        )

    @staticmethod
    def balance_info(user: Dict[str, Any]) -> str:
        return (
            f"{'='*35}\n"
            f"💰 *Управление балансом*\n"
            f"{'='*35}\n\n"
            f"💳 Доступно: *{user['balance']:,} KRW*\n"
            f"💎 Тариф: {'PRO' if user['is_pro'] else 'Базовый'}\n"
            f"📅 Срок PRO: {user['pro_expires'].split()[0] if user['pro_expires'] else '-'}\n\n"
            f"💡 *Действия с балансом:*\n"
            f"• Пополнение\n"
            f"• Вывод средств\n"
            f"• История операций\n"
            f"• Активация промокода\n"
            f"{'='*35}"
        ) 