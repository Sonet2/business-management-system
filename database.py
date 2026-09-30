import sqlite3
import os
class Database:
    def __init__(self, db_path):
        self.db_path = db_path or os.getenv("DATABASE")
        self.sqlconn = None
    def connect(self):
        if self.db_path is None or self.db_path.strip() == "":
            raise ValueError("db_path is empty")
        try:
            if self.sqlconn is None:
                self.sqlconn = sqlite3.connect(self.db_path)
                self.sqlconn.execute("PRAGMA foreign_keys = 1")
        except sqlite3.Error as error:
            self.sqlconn = None
            raise 
        return self.sqlconn
    def close(self):
        if self.sqlconn is not None:
            self.sqlconn.close()
            self.sqlconn = None
    