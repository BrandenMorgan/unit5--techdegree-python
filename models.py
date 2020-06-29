import datetime

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *


DATABASE = SqliteDatabase('learning_journal.db')

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, email, password):
        try:
            with DATABASE.transaction():
                cls.create(
                    username=username,
                    email=email,
                    password=generate_password_hash(password))

        except IntegrityError:
            raise ValueError("User already exists")


class Entry(Model):
    title = CharField(max_length=100)
    date_created = DateField(default=datetime.datetime.now)
    content = TextField()
    resources = TextField()
    time_spent = IntegerField()
    user = ForeignKeyField(User, backref='entries')

    class Meta:
        database = DATABASE


class Tag(Model):
    tags = TextField()
    to_entry = ForeignKeyField(Entry)

    class Meta:
        database = DATABASE
        index = (
            (('to_entry'), True),
        )


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry, User, Tag], safe=True)
    DATABASE.close()
