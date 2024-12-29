from enum import Enum, auto

class States(Enum):
    """Состояния разговора с ботом"""
    # Основные состояния
    MAIN_MENU = auto()
    CONTACT = auto()
    CITY = auto()
    
    # Состояния для объявлений
    ADS_MENU = auto()
    AD_TYPE = auto()
    AD_CONTENT = auto()
    AD_PHOTO = auto()
    AD_PRICE = auto()
    AD_HASHTAGS = auto()
    
    # Состояния профиля
    PROFILE_MENU = auto()
    CHANGE_CITY = auto()
    CHANGE_CONTACT = auto()
    SECURITY = auto()
    
    # Состояния баланса
    BALANCE_MENU = auto()
    ADD_BALANCE = auto()
    WITHDRAW = auto()
    WITHDRAW_METHOD = auto()
    WITHDRAW_AMOUNT = auto()
    
    # Состояния верификации
    VERIFICATION_DOCUMENT = auto()
    VERIFICATION_SELFIE = auto()
    VERIFICATION_ADDRESS = auto()
    
    # Состояния поиска
    SEARCH_MENU = auto()
    SEARCH_QUERY = auto()
    
    # Состояния помощи
    HELP_MENU = auto()
    SUPPORT_MESSAGE = auto()
    
    # Админские состояния
    ADMIN_MENU = auto()
    ADMIN_MODERATION = auto()
    ADMIN_VERIFICATION = auto()
    ADMIN_USERS = auto()
    ADMIN_FINANCE = auto()
    ADMIN_SETTINGS = auto() 