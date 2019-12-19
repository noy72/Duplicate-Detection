import sqlite3

from src.definition import ROOT


class Database:
    def __init__(self, table_name):
        self.table_name = table_name

    def save(self, data):
        conn = sqlite3.connect(f'{ROOT}/src/database/SQlite3')
        c = conn.cursor()
        c.execute(f'INSERT INTO {self.table_name} VALUES(?);', (data,))
        conn.commit()
        conn.close()

    def check(self, data):
        conn = sqlite3.connect(f'{ROOT}/src/database/SQlite3')
        c = conn.cursor()
        res = c.execute(f'SELECT * FROM {self.table_name} WHERE data=?;', (data,)).fetchone()
        conn.close()
        return res is not None

    def check_ids(self, data):
        conn = sqlite3.connect(f'{ROOT}/src/database/SQlite3')
        c = conn.cursor()

        results = []
        for d in data:
            res = c.execute(f'SELECT * FROM {self.table_name} WHERE data=?;', (d,)).fetchone()
            results.append(res is not None)
        conn.close()

        return results

    def delete(self):
        conn = sqlite3.connect(f'{ROOT}/src/database/SQlite3')
        c = conn.cursor()
        c.execute(f'DELETE FROM {self.table_name};')
        conn.commit()
        conn.close()
