import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="schedule.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            hour TEXT NOT NULL,
            task TEXT
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS memos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            memo TEXT
        )
        """)
        self.connection.commit()

    def save_schedule(self, date, hour, task):
        self.cursor.execute("""
        INSERT INTO schedules (date, hour, task) VALUES (?, ?, ?)
        ON CONFLICT(date, hour) DO UPDATE SET task=excluded.task
        """, (date, hour, task))
        self.connection.commit()

    def save_memo(self, date, memo):
        self.cursor.execute("""
        INSERT INTO memos (date, memo) VALUES (?, ?)
        ON CONFLICT(date) DO UPDATE SET memo=excluded.memo
        """, (date, memo))
        self.connection.commit()

    def load_schedule(self, date):
        self.cursor.execute("SELECT hour, task FROM schedules WHERE date=?", (date,))
        return {row[0]: row[1] for row in self.cursor.fetchall()}

    def load_memo(self, date):
        self.cursor.execute("SELECT memo FROM memos WHERE date=?", (date,))
        result = self.cursor.fetchone()
        return result[0] if result else ""

    def delete_schedule(self, date, hour):
        self.cursor.execute("DELETE FROM schedules WHERE date=? AND hour=?", (date, hour))
        self.connection.commit()

    def delete_memo(self, date):
        self.cursor.execute("DELETE FROM memos WHERE date=?", (date,))
        self.connection.commit()

    def close(self):
        self.connection.close()
