import sqlite3
from sqlite3 import Error

from bots.bot_class import Bot


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Database:
    def __init__(self, db):
        self.db = db
        self.sqliteConnection = None
        self.cursor = None
        self.open()

    def __del__(self):
        if self.sqliteConnection:
            self.close()

    def open(self):
        try:
            self.sqliteConnection = sqlite3.connect(self.db)
            self.sqliteConnection.row_factory = dict_factory
            self.cursor = self.sqliteConnection.cursor()
        except Error as e:
            print(e)

    def commit(self):
        self.sqliteConnection.commit()

    def close(self):
        self.cursor.execute("""VACUUM;""")
        self.commit()
        self.cursor.close()
        self.sqliteConnection.close()

    def add_bot(self, bot: Bot):
        try:
            if not self.sqliteConnection:
                self.open()
            query = """INSERT INTO bots (id,name,user_id,code) VALUES (?,?,?,?);"""
            data = (None, bot.name, bot.user_id, bot.code)
            self.cursor.execute(query, data)
            self.commit()
            self.cursor.execute("SELECT last_insert_rowid()")
            return self.cursor.fetchone()["last_insert_rowid()"]
        except sqlite3.Error as error:
            print(f"Error while adding bot", error)

    def get_bot(self, bot_id) -> Bot:
        try:
            if not self.sqliteConnection:
                self.open()
            query = """select * from bots where id == ?"""
            self.cursor.execute(query, (bot_id,))
            bot = self.cursor.fetchone()
            return Bot(bot["id"], bot["user_id"], bot["name"], bot["code"])
        except sqlite3.Error as error:
            print(f"Error while adding bot", error)
