import sqlite3

class SqliteDatabase(object):

    def __init__(self, db_file):
        self.db_file = db_file

    def create_connection(self):
        connection = sqlite3.connect(self.db_file, isolation_level=None)
        connection.execute('pragma journal_mode=wal;')
        return connection

    def run_non_query(self, query, binds=None):
        if binds is None:
            binds = []

        connection = self.create_connection()
        result = connection.execute(query, binds)
        connection.commit()
        return result

    def run_query(self, query, binds=None):
        if binds is None:
            binds = []

        return self.create_connection().execute(query, binds)