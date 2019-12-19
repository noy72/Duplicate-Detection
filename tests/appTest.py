import json
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

        html = resp.unicode_normal_body
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

    def test_allow_origin(self):
        resp = self.app.get('/')
        self.assertEqual(('Access-Control-Allow-Origin', '*'), resp.headerlist[0])

    def test_options(self):
        resp = self.app.options('/')
        self.assertEqual('200 OK', resp.status)
        self.assertEqual({}, resp.json)

    def test_api_exist(self):
        data = [uid(), uid(), uid()]

        form = self.app.get('/').form
        form['data'] = data[0]
        resp = form.submit()
        self.assertEqual('200 OK', resp.status)

        form['data'] = data[2]
        resp = form.submit()
        self.assertEqual('200 OK', resp.status)

        resp = self.app.post(
            '/api/exist',
            content_type='application/json',
            params=json.dumps({
                'data': data
            })
        )
        self.assertEqual({'data': [1, 0, 1]}, resp.json)


if __name__ == '__main__':
    unittest.main()
