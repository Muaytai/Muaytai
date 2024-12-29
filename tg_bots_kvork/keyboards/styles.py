from typing import List
from telegram import InlineKeyboardButton

class ButtonStyles:
    """Стили кнопок для разных разделов"""
    
    @staticmethod
    def main_menu_buttons() -> List[List[InlineKeyboardButton]]:
        return [
            [
                InlineKeyboardButton("📝 Подать объявление", callback_data="create_ad"),
                InlineKeyboardButton("🔍 Поиск", callback_data="search")
            ],
            [
                InlineKeyboardButton("👤 Профиль", callback_data="profile"),
                InlineKeyboardButton("💰 Баланс", callback_data="balance")
            ],
            [
                InlineKeyboardButton("📊 Мои объявления", callback_data="my_ads"),
                InlineKeyboardButton("ℹ️ Помощь", callback_data="help")
            ]
        ]
    
    @staticmethod
    def profile_buttons(is_verified: bool) -> List[List[InlineKeyboardButton]]:
        buttons = [
            [
                InlineKeyboardButton("🌆 Изменить город", callback_data="change_city"),
                InlineKeyboardButton("📱 Изменить контакт", callback_data="change_contact")
            ],
            [
                InlineKeyboardButton("📊 Статистика", callback_data="stats"),
                InlineKeyboardButton("⚙️ Настройки", callback_data="settings")
            ]
        ]
        
        if not is_verified:
            buttons.insert(0, [InlineKeyboardButton(
                "✅ Пройти верификацию", 
                callback_data="verify"
            )])
            
        buttons.append([InlineKeyboardButton(
            "🏠 Главное меню", 
            callback_data="main_menu"
        )])
        
        return buttons
    
    @staticmethod
    def ad_category_buttons() -> List[List[InlineKeyboardButton]]:
        return [
            [
                InlineKeyboardButton("🏠 Недвижимость", callback_data="cat_realty"),
                InlineKeyboardButton("💼 Работа", callback_data="cat_job")
            ],
            [
                InlineKeyboardButton("🚗 Транспорт", callback_data="cat_transport"),
                InlineKeyboardButton("📦 Товары", callback_data="cat_goods")
            ],
            [
                InlineKeyboardButton("🔧 Услуги", callback_data="cat_services"),
                InlineKeyboardButton("📢 Разное", callback_data="cat_other")
            ],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
        ] 