import datetime
from functools import wraps
import unittest

from peewee import *

import app
from models import User, Entry, Tag

MODELS = (User, Entry, Tag)
TEST_DB = SqliteDatabase(':memory:')

USER_DATA = {
    'email': 'test_0@example.com',
    'password': 'password'
}


def use_test_database(fn):
    @wraps(fn)
    def inner(self):
        with TEST_DB.bind_ctx(MODELS):
            TEST_DB.create_tables(MODELS)
            try:
                fn(self)
            finally:
                TEST_DB.drop_tables(MODELS)
    return inner


class UserModelTestCase(unittest.TestCase):
    @staticmethod
    def create_users(count=2):
        for i in range(count):
            User.create_user(
                username='{}'.format(i),
                email='test_{}@example.com'.format(i),
                password='password'
            )

    @use_test_database
    def test_create_user(self):
            self.create_users()
            self.assertEqual(User.select().count(), 2)
            self.assertNotEqual(
                User.select().get().password,
                'password'
            )

    @use_test_database
    def test_create_duplicate_user(self):
            self.create_users()
            with self.assertRaises(ValueError):
                User.create_user(
                    username='1',
                    email='test_1@example.com',
                    password='password'
                )


class EntryModelTestCase(unittest.TestCase):
    @use_test_database
    def test_entry_creation(self):
        UserModelTestCase.create_users()
        user = User.select().get()
        Entry.create(
            title='testing',
            content='testing entry',
            resources='resources test',
            time_spent=60,
            user=user
        )
        entry = Entry.select().get()

        self.assertEqual(
            Entry.select().count(),
            1
        )
        self.assertEqual(entry.user, user)

class ViewTestCase(unittest.TestCase):
    def setUp(self):
        app.app.config['TESTING'] = True
        app.app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.app.test_client()


class UserViewsTestCase(ViewTestCase):
    @use_test_database
    def test_registration(self):
        data = {
            'username': 'test',
            'email': 'test@example.com',
            'password': 'password',
            'password2': 'password'
        }

        rv = self.app.post(
            '/register',
            data=data)
        self.assertEqual(rv.status_code, 302)
        self.assertEqual(rv.location, 'http://localhost/entries')

    @use_test_database
    def test_good_login(self):
        UserModelTestCase.create_users(1)
        rv = self.app.post('/login', data=USER_DATA)
        self.assertEqual(rv.status_code, 302)
        self.assertEqual(rv.location, 'http://localhost/entries')

    @use_test_database
    def test_bad_login(self):
        rv = self.app.post('/login', data=USER_DATA)
        self.assertEqual(rv.status_code, 200)

    @use_test_database
    def test_logout(self):
        # Create and login the user
        UserModelTestCase.create_users(1)
        self.app.post('/login', data=USER_DATA)

        rv = self.app.get('/logout')
        self.assertEqual(rv.status_code, 302)
        self.assertEqual(rv.location, 'http://localhost/entries')

    @use_test_database
    def test_logged_out_menu(self):
        rv = self.app.get('/')
        self.assertIn("register", rv.get_data(as_text=True).lower())
        self.assertIn("log in", rv.get_data(as_text=True).lower())

    @use_test_database
    def test_logged_in_menu(self):
        UserModelTestCase.create_users(1)
        self.app.post('/login', data=USER_DATA)
        rv = self.app.get('/')
        self.assertIn("new entry", rv.get_data(as_text=True).lower())
        self.assertIn("log out", rv.get_data(as_text=True).lower())


class EntryViewsTestCase(ViewTestCase):
    @use_test_database
    def test_empty_db(self):
        rv = self.app.get('/')
        self.assertIn("no entries yet", rv.get_data(as_text=True).lower())

    @use_test_database
    def test_entry_list(self):
        entry_data = {
            'title': 'testing',
            'content': 'testing entry',
            'resources': 'resources',
            'time_spent': 60
        }
        UserModelTestCase.create_users(1)
        entry_data['user'] = User.select().get()
        Entry.create(**entry_data)

        rv = self.app.get('/')
        self.assertNotIn('no entries yet', rv.get_data(as_text=True))
        self.assertIn(entry_data['title'], rv.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
