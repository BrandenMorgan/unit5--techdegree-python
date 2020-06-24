import unittest

from playhouse.test_utils import test_database
from peewee import *

import app
from models import User, Entry

TEST_DB = SqliteDatabase(':memory:')
TEST_DB.connect()
TEST_DB.create_tables([User, Entry], safe=True)

class UserModelTestCase(unittest.TestCase):
    @staticmethod
    def create_users(count=2):
        for i in range(count):
            User.create_user(
                username='{}'.format(i),
                email='test_{}@example.com'.format(i),
                password='password'
            )

    def test_create_user(self):
        with test_database(TEST_DB, (User,)):
            self.create_users()
            self.assertEqual(User.select().count(), 2)
            self.assertNotEqual(
                User.select().get().password,
                'password'
            )

    def test_create_duplicate_user(self):
        with test_database(TEST_DB, (User,)):
            self.create_users()
            with self.assertRaises(ValueError):
                User.create_user(
                    username='1',
                    email='test_1@example.com',
                    password='password'
                )


if __name__ == "__main__":
    unittest.main()
