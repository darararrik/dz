import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="database/network_monitor.db"):
        self.db_name = db_name
        self._init_db()

    def _init_db(self):
        """Инициализация базы данных и создание таблиц"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            # Создаем таблицу для пингов
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Пинги (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    address TEXT NOT NULL,
                    timestamp DATETIME NOT NULL,
                    result TEXT NOT NULL
                )
            ''')
            
            # Создаем таблицу для трассировки
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Трассировки (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    address TEXT NOT NULL,
                    timestamp DATETIME NOT NULL,
                    result TEXT NOT NULL
                )
            ''')
            
            conn.commit()

    def save_ping(self, address, result):
        """Сохранение результата пинга"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(
                'INSERT INTO Пинги (address, timestamp, result) VALUES (?, ?, ?)',
                (address, current_time, result)
            )
            conn.commit()

    def save_trace(self, address, result):
        """Сохранение результата трассировки"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(
                'INSERT INTO Трассировки (address, timestamp, result) VALUES (?, ?, ?)',
                (address, current_time, result)
            )
            conn.commit()

    def get_ping_history(self, limit=10):
        """Получение истории пингов"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT address, timestamp, result FROM Пинги ORDER BY timestamp DESC LIMIT ?',
                (limit,)
            )
            return cursor.fetchall()

    def get_trace_history(self, limit=10):
        """Получение истории трассировок"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT address, timestamp, result FROM Трассировки ORDER BY timestamp DESC LIMIT ?',
                (limit,)
            )
            return cursor.fetchall() 