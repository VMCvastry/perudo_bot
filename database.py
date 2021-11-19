import os
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
            if not os.path.isfile(self.db):
                raise Exception("WORNG DB PATH")
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
            query = "INSERT INTO bots (id,name,user_id,code, victory, defeat) VALUES (?,?,?,?,?,?);"
            data = (None, bot.name, bot.user_id, bot.code, bot.victory, bot.defeat)
            self.cursor.execute(query, data)
            self.commit()
            self.cursor.execute("SELECT last_insert_rowid()")
            return self.cursor.fetchone()["last_insert_rowid()"]
        except sqlite3.Error as error:
            print(f"Error while adding bot", error)

    def add_victory(self, bot_id):
        try:
            if not self.sqliteConnection:
                self.open()
            query = "UPDATE bots SET victory = victory + 1 WHERE id = ?"
            data = (bot_id,)
            self.cursor.execute(query, data)
            self.commit()
        except sqlite3.Error as error:
            print(f"Error while incrementig victory bot", error)

    def add_defeat(self, bot_id):
        try:
            if not self.sqliteConnection:
                self.open()
            query = "UPDATE bots SET defeat = defeat + 1 WHERE id = ?"
            data = (bot_id,)
            self.cursor.execute(query, data)
            self.commit()
        except sqlite3.Error as error:
            print(f"Error while incrementig defeat bot", error)

    def get_bot(self, bot_id) -> Bot:
        try:
            if not self.sqliteConnection:
                self.open()
            query = "select * from bots where id == ?"
            self.cursor.execute(query, (bot_id,))
            bot = self.cursor.fetchone()
            return Bot(
                bot["id"],
                bot["name"],
                bot["user_id"],
                bot["code"],
                bot["victory"],
                bot["defeat"],
            )
        except sqlite3.Error as error:
            print(f"Error while getting bot", error)

    def get_all_bots(self) -> list[Bot]:
        try:
            if not self.sqliteConnection:
                self.open()
            query = """select * from bots"""
            self.cursor.execute(query)
            bots = self.cursor.fetchall()
            return [
                Bot(
                    bot["id"],
                    bot["name"],
                    bot["user_id"],
                    bot["code"],
                    bot["victory"],
                    bot["defeat"],
                )
                for bot in bots
            ]
        except sqlite3.Error as error:
            print(f"Error while getting all bots", error)
