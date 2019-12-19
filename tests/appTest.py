import unittest

from webtest import TestApp

from src.app import app
from src.util.string import uid


class TestAppMethods(unittest.TestCase):
    def setUp(self):
        self.app = TestApp(app)

    def exist(self, html, tag):
        self.assertNotEqual(-1, html.find(tag))

    def notExist(self, html, tag):
        self.assertEqual(-1, html.find(tag))

    def test_get_index(self):
        resp = self.app.get('/')
        self.assertEqual('200 OK', resp.status)

        html = resp.body.decode()
        self.exist(html, '<button>submit</button>')
        self.notExist(html, '<h2>Duplicated!!!</h2>')
        self.notExist(html, '<h2>Saved</h2>')

    def test_post_index(self):
        data = uid()
        for status in ['save', 'duplicated']:
            form = self.app.get('/').form

            form['data'] = data
            resp = form.submit()

            self.assertEqual('200 OK', resp.status)

            html = resp.body.decode()
            self.exist(html, '<button>submit</button>')

            if status == 'save':
                self.notExist(html, '<h2>Duplicated!!!</h2>')
                self.exist(html, '<h2>Saved</h2>')
            else:
                self.notExist(html, '<h2>Saved</h2>')
                self.exist(html, '<h2>Duplicated!!!</h2>')


if __name__ == '__main__':
    unittest.main()
