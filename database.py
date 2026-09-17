import sqlite3
import os
class Database:
    def __init__(self, db_path):
        self.db_path = db_path or os.getenv("DATABASE")
    def connection(self, db_path):
        if db_path is None or db_path.strip == "":
            return None
        try:
            sqlconn = sqlite3.connect(db_path)
            cur = sqlconn.cursor()
        except sqlite3.Error as error:
            print('Error occurred -', error)
        