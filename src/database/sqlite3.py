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
        data = data.strip()
        try:
            c.execute(f'INSERT INTO {self.table_name} VALUES(?);', (data,))
        except sqlite3.IntegrityError:
            conn.close()
            return False
        else:
            conn.commit()
            conn.close()
            return True

    def save_many(self, data):
        conn, c = self._connect_db()
        t_data = []
        for d in data:
            t_data.append((d,))

        try:
            c.executemany(f'INSERT INTO {self.table_name} VALUES(?)', t_data)
        except sqlite3.IntegrityError:
            conn.close()
            return False
        else:
            conn.commit()
            conn.close()
            return True

    def exist(self, data):
        conn, c = self._connect_db()

        results = []
        for d in data:
            res = c.execute(f'SELECT EXISTS (select * from {self.table_name} where data like ?);',
                            (f'%{d}%',)).fetchone()
            results.append(res[0])
        conn.close()

        return results

    def get_all_data(self):
        conn, c = self._connect_db()

        res = c.execute(f'select * from {self.table_name};').fetchall()
        conn.close()

        return res

    def delete(self):
        conn, c = self._connect_db()
        c.execute(f'DELETE FROM {self.table_name};')
        conn.commit()
        conn.close()
