import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('schedule.db')
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        try:
            # 创建 schedule 表，包含起始和结束时间的小时和分钟
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS schedule (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    start_hour INTEGER NOT NULL,
                    start_minute INTEGER NOT NULL,
                    end_hour INTEGER NOT NULL,
                    end_minute INTEGER NOT NULL,
                    task_name TEXT NOT NULL,
                    is_completed INTEGER DEFAULT 0)
            ''')
            self.conn.commit()
        except Exception as e:
            print("创建表失败:", e)
        finally:
            cursor.close()

    def save_schedule(self, date, start_hour, start_minute, end_hour, end_minute, task_name):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO schedule (date, start_hour, start_minute, end_hour, end_minute, task_name, is_completed)
                VALUES (?, ?, ?, ?, ?, ?, 0)
            ''', (date, start_hour, start_minute, end_hour, end_minute, task_name))
            self.conn.commit()
        except Exception as e:
            print("保存日程失败:", e)
        finally:
            cursor.close()

    def load_schedule(self, date):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                SELECT start_hour, start_minute, end_hour, end_minute, task_name, is_completed
                FROM schedule WHERE date=?
            ''', (date,))
            return cursor.fetchall()
        except Exception as e:
            print("加载日程失败:", e)
            return []
        finally:
            cursor.close()

    def delete_schedule(self, date, start_hour=None, start_minute=None):
        cursor = self.conn.cursor()
        try:
            if start_hour is not None and start_minute is not None:
                # 删除特定开始时间的日程
                cursor.execute('''
                    DELETE FROM schedule WHERE date=? AND start_hour=? AND start_minute=?
                ''', (date, start_hour, start_minute))
            else:
                # 删除该日期的所有日程
                cursor.execute("DELETE FROM schedule WHERE date=?", (date,))
            print(f"已删除的行数: {cursor.rowcount}")
            self.conn.commit()
        except Exception as e:
            print("删除日程失败:", e)
        finally:
            cursor.close()

    def close(self):
        self.conn.close()
