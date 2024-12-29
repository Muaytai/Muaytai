import sqlite3
from datetime import datetime, timedelta
import os

class Database:
    def __init__(self, db_file: str):
        """Инициализация соединения с базой данных"""
        self.db_file = db_file
        self.conn = None
        self.connect()
        
    def connect(self):
        """Установка соединения с базой данных"""
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.conn.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            print(f"Ошибка подключения к базе данных: {e}")
            
    def init_db(self):
        """Инициализация структуры базы данных"""
        try:
            with self.conn:
                self.conn.executescript('''
                    CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        username TEXT,
                        phone TEXT,
                        city TEXT,
                        balance INTEGER DEFAULT 0,
                        is_pro BOOLEAN DEFAULT FALSE,
                        is_verified BOOLEAN DEFAULT FALSE,
                        verification_requested BOOLEAN DEFAULT FALSE,
                        registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        last_post DATETIME,
                        pro_expires DATETIME
                    );

                    CREATE TABLE IF NOT EXISTS ads (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        type TEXT,
                        city TEXT,
                        content TEXT,
                        image_file_id TEXT,
                        price TEXT,
                        hashtags TEXT,
                        status TEXT DEFAULT 'pending',
                        views INTEGER DEFAULT 0,
                        clicks INTEGER DEFAULT 0,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        expires_at DATETIME,
                        FOREIGN KEY (user_id) REFERENCES users (user_id)
                    );

                    CREATE TABLE IF NOT EXISTS verifications (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        document_photo TEXT,
                        selfie_photo TEXT,
                        address TEXT,
                        status TEXT DEFAULT 'pending',
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (user_id)
                    );

                    CREATE TABLE IF NOT EXISTS payments (
                        payment_id TEXT PRIMARY KEY,
                        user_id INTEGER,
                        amount INTEGER,
                        type TEXT,
                        status TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (user_id)
                    );
                ''')
        except sqlite3.Error as e:
            print(f"Ошибка инициализации базы данных: {e}")

    def execute(self, query: str, params: tuple = None):
        """Выполнение SQL-запроса"""
        try:
            if not self.conn:
                self.connect()
            with self.conn:
                if params:
                    return self.conn.execute(query, params)
                return self.conn.execute(query)
        except sqlite3.Error as e:
            print(f"Ошибка выполнения запроса: {e}")
            return None 

    def get_user(self, user_id: int) -> dict:
        """Получает информацию о пользователе"""
        try:
            cursor = self.conn.execute("""
                SELECT user_id, username, phone, city, balance, 
                       is_pro, is_verified, verification_requested,
                       registration_date, last_post, pro_expires
                FROM users 
                WHERE user_id = ?
            """, (user_id,))
            user = cursor.fetchone()
            
            if user:
                return dict(user)
            return None
            
        except Exception as e:
            print(f"Ошибка при получении пользователя: {e}")
            return None

    def add_user(self, user_id: int, username: str, phone: str = None, city: str = None) -> bool:
        """Добавляет нового пользователя"""
        try:
            with self.conn:
                # Проверяем существование пользователя
                cursor = self.conn.execute(
                    "SELECT user_id FROM users WHERE user_id = ?", 
                    (user_id,)
                )
                if cursor.fetchone():
                    return False
                
                # Добавляем нового пользователя
                self.conn.execute("""
                    INSERT INTO users (
                        user_id, username, phone, city, 
                        registration_date
                    ) VALUES (?, ?, ?, ?, datetime('now'))
                """, (user_id, username, phone, city))
                return True
                
        except Exception as e:
            print(f"Ошибка при добавлении пользователя: {e}")
            return False

    def update_user(self, user_id: int, **kwargs) -> bool:
        """Обновляет данные пользователя"""
        try:
            with self.conn:
                fields = []
                values = []
                
                for key, value in kwargs.items():
                    fields.append(f"{key} = ?")
                    values.append(value)
                
                if not fields:
                    return False
                    
                values.append(user_id)
                query = f"""
                    UPDATE users 
                    SET {', '.join(fields)}
                    WHERE user_id = ?
                """
                
                self.conn.execute(query, values)
                return True
                
        except Exception as e:
            print(f"Ошибка при обновлении пользователя: {e}")
            return False

    def get_cities(self) -> list:
        """Возвращает список городов"""
        try:
            cursor = self.conn.execute(
                "SELECT DISTINCT city FROM users WHERE city IS NOT NULL ORDER BY city"
            )
            return cursor.fetchall()
        except Exception as e:
            print(f"Ошибка при получении списка городов: {e}")
            return [] 

    def city_exists(self, city: str) -> bool:
        """Проверяет существование города в базе данных"""
        # Всегда возвращаем True, так как теперь разрешаем любые города
        return True

    def add_city(self, city: str) -> bool:
        """Добавляет новый город в базу данных"""
        try:
            with self.conn:
                self.conn.execute(
                    "INSERT INTO cities (name) VALUES (?)",
                    (city,)
                )
                return True
        except Exception as e:
            print(f"Ошибка при добавлении города: {e}")
            return False 

    def can_post_free_ad(self, user_id: int) -> bool:
        """Проверяет, может ли пользователь разместить бесплатное объявление"""
        try:
            user = self.get_user(user_id)
            if not user:
                return False
            
            # PRO пользователи могут размещать без ограничений
            if user['is_pro']:
                return True
            
            # Проверяем количество активных объявлений
            cursor = self.conn.execute("""
                SELECT COUNT(*) FROM ads 
                WHERE user_id = ? 
                AND status = 'published'
                AND created_at > datetime('now', '-24 hours')
            """, (user_id,))
            
            active_ads = cursor.fetchone()[0]
            return active_ads < 3  # Максимум 3 бесплатных объявления в сутки
            
        except Exception as e:
            print(f"Ошибка при проверке возможности размещения объявления: {e}")
            return False

    def get_user_ads_count(self, user_id: int) -> dict:
        """Получает статистику объявлений пользователя"""
        try:
            cursor = self.conn.execute("""
                SELECT 
                    COUNT(*) FILTER (WHERE status = 'published') as active,
                    COUNT(*) FILTER (WHERE status = 'pending') as pending,
                    COUNT(*) FILTER (WHERE status = 'rejected') as rejected,
                    COUNT(*) FILTER (WHERE created_at > datetime('now', '-24 hours')) as today
                FROM ads 
                WHERE user_id = ?
            """, (user_id,))
            
            result = cursor.fetchone()
            return {
                'active': result[0],
                'pending': result[1],
                'rejected': result[2],
                'today': result[3]
            }
            
        except Exception as e:
            print(f"Ошибка при получении статистики объявлений: {e}")
            return {'active': 0, 'pending': 0, 'rejected': 0, 'today': 0} 

    def create_ad(self, user_id: int, ad_type: str, city: str, content: str, 
                  image_file_id: str = None, price: str = None, hashtags: str = None) -> int:
        """Создает новое объявление"""
        try:
            with self.conn:
                # Проверяем и форматируем хештеги
                if hashtags:
                    # Убираем символ # если он есть в начале
                    formatted_tags = ' '.join([
                        tag.lstrip('#') for tag in hashtags.split()
                    ])
                else:
                    formatted_tags = None

                cursor = self.conn.execute("""
                    INSERT INTO ads (
                        user_id, type, city, content,
                        image_file_id, price, hashtags,
                        status, created_at, expires_at
                    ) VALUES (
                        ?, ?, ?, ?, ?, ?, ?, 
                        'pending',
                        datetime('now'),
                        datetime('now', '+30 days')
                    )
                """, (
                    user_id, ad_type, city, content,
                    image_file_id, price, formatted_tags
                ))
                
                ad_id = cursor.lastrowid
                
                # Обновляем время последней публикации пользователя
                self.conn.execute("""
                    UPDATE users 
                    SET last_post = datetime('now')
                    WHERE user_id = ?
                """, (user_id,))
                
                return ad_id
                
        except Exception as e:
            print(f"Ошибка при создании объявления: {e}")
            return None

    def get_ad(self, ad_id: int) -> dict:
        """Получает информацию об объявлении"""
        try:
            cursor = self.conn.execute("""
                SELECT id, user_id, type, city, content,
                       image_file_id, price, hashtags,
                       status, views, clicks, 
                       created_at, expires_at
                FROM ads 
                WHERE id = ?
            """, (ad_id,))
            ad = cursor.fetchone()
            
            if ad:
                return dict(ad)
            return None
            
        except Exception as e:
            print(f"Ошибка при получении объявления: {e}")
            return None

    def get_user_ads(self, user_id: int, status: str = None) -> list:
        """Получает объявления пользователя"""
        try:
            query = """
                SELECT id, type, city, content,
                       image_file_id, price, hashtags,
                       status, views, clicks, created_at
                FROM ads 
                WHERE user_id = ?
            """
            params = [user_id]
            
            if status:
                query += " AND status = ?"
                params.append(status)
                
            query += " ORDER BY created_at DESC"
            
            cursor = self.conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
            
        except Exception as e:
            print(f"Ошибка при получении объявлений пользователя: {e}")
            return [] 

    def update_ad_status(self, ad_id: int, status: str) -> bool:
        """Обновляет статус объявления"""
        try:
            with self.conn:
                self.conn.execute(
                    "UPDATE ads SET status = ? WHERE id = ?",
                    (status, ad_id)
                )
                return True
        except Exception as e:
            print(f"Ошибка при обновлении статуса объявления: {e}")
            return False 