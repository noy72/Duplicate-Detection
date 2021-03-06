import json
import unittest

from webtest import TestApp

from src.app import app
from src.database.sqlite3 import Database
from src.definition import TABLES
from src.util.string import uid


class TestAppMethods(unittest.TestCase):
    def setUp(self):
        self.app = TestApp(app)

    def test_get_index(self):
        resp = self.app.get('/')
        self.assertEqual('200 OK', resp.status)

        resp.mustcontain('<button>submit</button>')
        resp.mustcontain(no='<h2>Duplicated!!!</h2>')
        resp.mustcontain(no='<h2>Saved</h2>')

    def test_post_data_to_index(self):
        data = uid()
        for status in ['save', 'duplicated']:
            form = self.app.get('/').form

            form['data'] = data
            resp = form.submit()

            self.assertEqual('200 OK', resp.status)
            resp.mustcontain('<button>submit</button>')

            if status == 'save':
                resp.mustcontain('<h2>Saved</h2>')
                resp.mustcontain(no='<h2>Duplicated!!!</h2>')
            else:
                resp.mustcontain(no='<h2>Saved</h2>')
                resp.mustcontain('<h2>Duplicated!!!</h2>')

    def test_add_allow_origin(self):
        resp = self.app.get('/')
        self.assertEqual(('Access-Control-Allow-Origin', '*'), resp.headerlist[0])

        resp = self.app.post(
            '/api/exist',
            content_type='application/json',
            params=json.dumps({
                'data': ['a', 'b']
            })
        )
        self.assertEqual(('Access-Control-Allow-Origin', '*'), resp.headerlist[1])

    def test_options_work(self):
        resp = self.app.options('/')
        self.assertEqual('200 OK', resp.status)
        self.assertEqual({}, resp.json)

    def test_api_exist_work(self):
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

    def test_api_exist_substring(self):
        data = ['1234', '123']

        form = self.app.get('/').form
        form['data'] = data[0]
        resp = form.submit()
        self.assertEqual('200 OK', resp.status)

        resp = self.app.post(
            '/api/exist',
            content_type='application/json',
            params=json.dumps({
                'data': data
            })
        )
        self.assertEqual({'data': [1, 1]}, resp.json)

    def test_api_post(self):
        data = [uid(), uid(), uid()]

        resp = self.app.post(
            '/api/post',
            content_type='application/json',
            params=json.dumps({
                'data': data
            })
        )
        self.assertEqual('200 OK', resp.status)

        resp = self.app.post(
            '/api/exist',
            content_type='application/json',
            params=json.dumps({
                'data': data
            })
        )
        self.assertEqual({'data': [1, 1, 1]}, resp.json)


class TESTDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database(TABLES.test)

    def test_save_many(self):
        data = [uid(), uid(), uid()]
        self.assertEqual(True, self.db.save_many(data))
        self.assertEqual([1, 1, 1], self.db.exist(data))


if __name__ == '__main__':
    unittest.main()
