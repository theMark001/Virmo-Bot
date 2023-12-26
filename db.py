import sqlite3
from threading import Lock

class DatabaseHandler:
    def __init__(self, db_name='database.db'):
        self.db_name = db_name
        self.lock = Lock()
        self.initialize_database()

    def initialize_database(self):
        with self.lock:
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()

            # Создаем таблицу users, если она не существует
            cursor.execute('''CREATE TABLE IF NOT EXISTS users
                              (id INTEGER PRIMARY KEY, user_id INTEGER)''')

            # Создаем таблицу records, если она не существует
            cursor.execute('''CREATE TABLE IF NOT EXISTS records
                              (id INTEGER PRIMARY KEY, user_id INTEGER, lvl INTEGER, exp NUMERIC, wbd_lvl INTEGER, wbd_exp NUMERIC)''')

            connection.commit()

    def get_user_data(self, user_id):
        with self.lock:
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()
            cursor.execute("SELECT lvl, exp, wbd_lvl, wbd_exp FROM records WHERE user_id=?", (user_id,))
            data = cursor.fetchone()
            connection.close()
            return data if data else (0, 0, 0, 0)

    def update_user_data(self, user_id, exp, lvl, wbd_exp, wbd_lvl):
        with self.lock:
            connection = sqlite3.connect(self.db_name)
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM users WHERE user_id=?", (user_id,))
            user_exists = cursor.fetchone()

            if not user_exists:
                cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))

            cursor.execute("SELECT id FROM records WHERE user_id=?", (user_id,))
            record_id = cursor.fetchone()

            if record_id:
                cursor.execute("UPDATE records SET lvl=?, exp=?, wbd_exp=?, wbd_lvl=? WHERE user_id=?", (lvl, exp, wbd_exp, wbd_lvl, user_id))
            else:
                cursor.execute("INSERT INTO records (user_id, lvl, exp, wbd_lvl, wbd_exp) VALUES (?, ?, ?, ?, ?)", (user_id, lvl, exp, wbd_lvl, wbd_exp))

            connection.commit()
            connection.close()
