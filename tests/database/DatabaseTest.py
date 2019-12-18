import unittest
import uuid

from definition import TABLES
from src.database.Database import Database


def uid():
    return str(uuid.uuid1())


class TestDatabaseMethods(unittest.TestCase):

    def setUp(self):
        self.db = Database(TABLES.test)

    def tearDown(self):
        self.db.delete()

    def test_save(self):
        self.db.save(uid())

    def test_check(self):
        data = uid()
        self.db.save(data)
        self.assertTrue(self.db.check(data))
        self.assertFalse(self.db.check(uid()))

    def test_check_ids(self):
        data = [uid(), uid(), uid()]
        self.db.save(data[0])
        self.db.save(data[2])

        res = self.db.check_ids(data)
        self.assertEqual([1, 0, 1], res)


if __name__ == '__main__':
    unittest.main()
