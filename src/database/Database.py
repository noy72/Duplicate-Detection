import sqlite3

from src.definition import ROOT


class Database:
    def __init__(self, table_name):
        self.table_name = table_name
        self.path = f'{ROOT}/database/SQlite3'

    def _connect_db(self):
        conn = sqlite3.connect(self.path)
        c = conn.cursor()
        return conn, c

    def save(self, data):
        conn, c = self._connect_db()
        c.execute(f'INSERT INTO {self.table_name} VALUES(?);', (data,))
        conn.commit()
        conn.close()

    def exist(self, data):
        conn, c = self._connect_db()
        res = c.execute(f'SELECT EXISTS (select * from {self.table_name} where data=?);', (data,)).fetchone()
        conn.close()
        return res[0]

    def check_ids(self, data):
        conn, c = self._connect_db()

        results = []
        for d in data:
            res = c.execute(f'SELECT * FROM {self.table_name} WHERE data=?;', (d,)).fetchone()
            results.append(res is not None)
        conn.close()

        return results

    def delete(self):
        conn, c = self._connect_db()
        c.execute(f'DELETE FROM {self.table_name};')
        conn.commit()
        conn.close()
