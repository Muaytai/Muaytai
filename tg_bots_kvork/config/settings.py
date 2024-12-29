from os import getenv
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# Основные настройки
BOT_TOKEN = getenv('BOT_TOKEN')
ADMIN_USERNAME = getenv('ADMIN_USERNAME')
CHANNEL_ID = int(getenv('CHANNEL_ID'))  # Преобразуем в int, так как это ID канала

# Настройки PRO-аккаунта
PRO_PRICES = {
    '1_month': 50000,   # 1 месяц
    '3_months': 135000, # 3 месяца
    '6_months': 240000, # 6 месяцев
    '12_months': 420000 # 12 месяцев
}

# Настройки для объявлений
AD_SETTINGS = {
    'min_length': 20,  # Минимальная длина текста объявления
    'max_length': 1000,  # Максимальная длина текста объявления
    'free_interval': 3,  # Интервал между бесплатными объявлениями (в часах)
    'max_photos': 5,  # Максимальное количество фото
    'max_active': 10,  # Максимальное количество активных объявлений
}

# Категории объявлений
AD_CATEGORIES = {
    '🏠 Недвижимость': {
        'id': 'realty',
        'icon': '🏠',
        'description': 'Аренда и продажа недвижимости'
    },
    '💼 Работа': {
        'id': 'job',
        'icon': '💼',
        'description': 'Вакансии и поиск работы'
    },
    '🚗 Транспорт': {
        'id': 'transport',
        'icon': '🚗',
        'description': 'Продажа и аренда транспорта'
    },
    '📦 Товары': {
        'id': 'goods',
        'icon': '📦',
        'description': 'Продажа товаров'
    },
    '🔧 Услуги': {
        'id': 'services',
        'icon': '🔧',
        'description': 'Предложение услуг'
    },
    '📢 Разное': {
        'id': 'other',
        'icon': '📢',
        'description': 'Другие объявления'
    }
}

# Города
CITIES = [
    "Сеул",
    "Пусан",
    "Инчхон",
    "Тэгу",
    "Тэджон",
    "Кванджу",
    "Сувон",
    "Чхонан"
] 