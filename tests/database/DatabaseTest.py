import unittest

from src.database.Database import Database
from src.util.string import uid


class TestDatabaseMethods(unittest.TestCase):

    def setUp(self):
        self.db = Database('test')

    def tearDown(self):
        self.db.delete()

    def test_save(self):
        data = uid()
        self.assertTrue(self.db.save(data))
        self.assertFalse(self.db.save(data))

    def test_exist(self):
        data = [uid(), uid(), uid()]
        self.db.save(data[0])
        self.db.save(data[2])

        res = self.db.exist(data)
        self.assertEqual([1, 0, 1], res)


if __name__ == '__main__':
    unittest.main()
