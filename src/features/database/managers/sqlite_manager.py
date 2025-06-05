import sqlite3
import os
from config.resource_path import resource_path

class SqliteManager:
    _instance = None
    required_migration = False

    def __new__(cls, db_file='database.sqlite'):
        if cls._instance is None:
            cls._instance = super(SqliteManager, cls).__new__(cls)
            cls._instance._initialize(db_file)
        return cls._instance

    def _initialize(self, db_file):
        self.db_file = resource_path('assets', 'database', db_file)
        if not os.path.exists(self.db_file):
            self.required_migration = True
        self.conn = None

    def get_connection(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_file)
        return self.conn

    def close_connection(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def is_connection_open(self):
        if self.conn is None:
            return False
        try:
            self.conn.cursor()
            return True
        except sqlite3.ProgrammingError:
          return False