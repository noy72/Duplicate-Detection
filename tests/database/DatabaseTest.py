import unittest

from src.database.Database import Database
from src.util.string import uid


class TestDatabaseMethods(unittest.TestCase):

    def setUp(self):
        self.db = Database('test')

    def tearDown(self):
        self.db.delete()

    def test_save(self):
        self.db.save(uid())

    def test_check(self):
        data = uid()
        self.db.save(data)
        self.assertTrue(self.db.exist(data))
        self.assertFalse(self.db.exist(uid()))

    def test_check_ids(self):
        data = [uid(), uid(), uid()]
        self.db.save(data[0])
        self.db.save(data[2])

        res = self.db.check_ids(data)
        self.assertEqual([1, 0, 1], res)


if __name__ == '__main__':
    unittest.main()
