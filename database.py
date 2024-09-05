import sqlite3
from datetime import datetime

# Database 类负责管理数据库的连接、表结构的创建以及对数据库的各种操作（如插入、查询、更新、删除）。
class Database:
    # __init__ 方法：
    def __init__(self, db_name="schedule.db"): # db_name：数据库文件的名称，默认为schedule.db。这是一个SQLite数据库文件。
        self.connection = sqlite3.connect(db_name) # self.connection：与SQLite数据库的连接。
        self.cursor = self.connection.cursor() # self.cursor：数据库游标，用于执行SQL命令。
        self.create_tables() # self.create_tables()：调用方法创建所需的数据库表格。

    # create_tables() 方法：
    def create_tables(self):
        # schedules 表：用于存储日程安排，每个记录包含id、date（日期）、hour（小时）、task（任务描述）。
        # CREATE TABLE IF NOT EXISTS：如果表格不存在，则创建表格。
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            hour TEXT NOT NULL,
            task TEXT
        )
        """)
        # memos 表：用于存储备忘录，每个记录包含id、date（日期）、memo（备忘录内容）。
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS memos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            memo TEXT
        )
        """)
        # self.connection.commit()：提交事务，确保对数据库的更改被保存。
        self.connection.commit()

    # save_schedule() 方法：
    def save_schedule(self, date, hour, task): # 插入数据：将日程信息插入到schedules表中。
        # ON CONFLICT 子句：如果date和hour组合已经存在，则更新相应的任务内容task。
        self.cursor.execute("""
        INSERT INTO schedules (date, hour, task) VALUES (?, ?, ?)
        ON CONFLICT(date, hour) DO UPDATE SET task=excluded.task 
        """, (date, hour, task))
        # self.connection.commit()：提交事务，保存更改。
        self.connection.commit()

    # save_memo() 方法：
    def save_memo(self, date, memo): # 插入数据：将备忘录内容插入到memos表中。
        # ON CONFLICT 子句：如果date已经存在，则更新相应的备忘录内容。
        self.cursor.execute("""
        INSERT INTO memos (date, memo) VALUES (?, ?)
        ON CONFLICT(date) DO UPDATE SET memo=excluded.memo
        """, (date, memo))
        # self.connection.commit()：提交事务，保存更改。
        self.connection.commit()

    # load_schedule() 方法：
    def load_schedule(self, date):
        self.cursor.execute("SELECT hour, task FROM schedules WHERE date=?", (date,)) # 查询数据：根据日期查询schedules表中的所有记录。
        return {row[0]: row[1] for row in self.cursor.fetchall()} # self.cursor.fetchall()：获取所有查询结果。返回结果：以字典形式返回结果，键为hour，值为对应的task。

    # load_memo() 方法：
    def load_memo(self, date):
        self.cursor.execute("SELECT memo FROM memos WHERE date=?", (date,)) # 查询数据：根据日期查询memos表中的备忘录内容。
        result = self.cursor.fetchone() # self.cursor.fetchone()：获取单个查询结果（如果存在）。
        return result[0] if result else "" # 返回结果：如果查询结果存在，返回备忘录内容，否则返回空字符串。

    # delete_schedule() 方法：
    def delete_schedule(self, date, hour):
        self.cursor.execute("DELETE FROM schedules WHERE date=? AND hour=?", (date, hour)) # 删除数据：根据日期和小时删除schedules表中的记录。
        self.connection.commit() # self.connection.commit()：提交事务，保存更改。

    # delete_memo() 方法：
    def delete_memo(self, date):
        self.cursor.execute("DELETE FROM memos WHERE date=?", (date,)) # 删除数据：根据日期删除memos表中的记录。
        self.connection.commit() # self.connection.commit()：提交事务，保存更改。

    # close() 方法：
    def close(self):
        self.connection.close()# 关闭连接：关闭数据库连接，释放资源。
