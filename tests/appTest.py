import unittest

from src import app


class TestAppMethods(unittest.TestCase):
    def test_get_index(self):
        resp = app.index()
        self.assertNotEqual(resp.find("<button>submit</button>"), -1)
        self.assertEqual(resp.find("<h2>Duplicated!!!</h2>"), -1)
        self.assertEqual(resp.find("<h2>Saved</h2>"), -1)
