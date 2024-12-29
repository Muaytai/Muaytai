import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import Database
from datetime import datetime, timedelta

def create_test_data():
    db = Database('board.db')
    
    # Удаляем старую базу данных
    db.drop_db()
    
    # Создаем новую структуру
    db.init_db()
    
    # Добавляем начальные города
    initial_cities = [
        "Seoul", "Busan", "Incheon", "Daegu", "Daejeon",
        "Gwangju", "Ulsan", "Suwon", "Changwon", "Goyang"
    ]
    
    for city in initial_cities:
        db.add_city(city)
    
    # Создаем тестовых пользователей
    test_users = [
        (123456, "test_user1", "+82101234567", "Seoul", 100000),
        (234567, "test_user2", "+82109876543", "Busan", 50000),
        (345678, "test_admin", "+82105555555", "Seoul", 999999),
    ]
    
    for user_id, username, phone, city, balance in test_users:
        db.add_user(user_id, username, phone, city)
        db.execute("""
            UPDATE users 
            SET balance = ?,
                is_pro = CASE WHEN user_id = 345678 THEN TRUE ELSE FALSE END,
                is_verified = CASE WHEN user_id = 345678 THEN TRUE ELSE FALSE END
            WHERE user_id = ?
        """, (balance, user_id))
    
    # Создаем тестовые объявления
    test_ads = [
        (123456, "realty", "Seoul", "Сдается квартира 2+1\nРайон Каннам\nЦена договорная", None, "2,500,000", "квартира аренда каннам"),
        (234567, "job", "Busan", "Требуется официант\nОпыт не требуется\nЗП от 2.000.000", None, "2,000,000", "работа ресторан"),
        (123456, "services", "Seoul", "Уроки корейского языка\nНоситель языка\n1час = 50.000", None, "50,000", "корейский язык обучение")
    ]
    
    for user_id, ad_type, city, content, image, price, tags in test_ads:
        db.add_ad(user_id, ad_type, city, content, image, price, tags)
    
    # Создаем заявки на верификацию
    test_verifications = [
        (234567, "doc_photo_id_1", "selfie_photo_id_1", "Seoul, Gangnam-gu, 123-45"),
        (123456, "doc_photo_id_2", "selfie_photo_id_2", "Busan, Haeundae-gu, 67-89")
    ]
    
    for user_id, doc, selfie, address in test_verifications:
        db.create_verification_request(user_id, doc, selfie, address)
    
    # Создаем тестовые платежи
    test_payments = [
        ("PAY123", 123456, 50000, "deposit", "completed"),
        ("PAY234", 234567, 100000, "deposit", "pending"),
        ("PAY345", 123456, 30000, "withdraw", "completed")
    ]
    
    for payment_id, user_id, amount, type, status in test_payments:
        db.execute("""
            INSERT INTO payments (payment_id, user_id, amount, type, status)
            VALUES (?, ?, ?, ?, ?)
        """, (payment_id, user_id, amount, type, status))
    
    print("✅ Тестовые данные успешно созданы")

if __name__ == "__main__":
    create_test_data() 