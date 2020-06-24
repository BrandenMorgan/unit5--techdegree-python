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
    date_created = DateTimeField(default=datetime.datetime.now)
    title = CharField(max_length=100)
    content = TextField()
    resources = TextField()
    time_spent = IntegerField()
    user = ForeignKeyField(User, backref='entries')

    class Meta:
        database = DATABASE
        # order_by = ('date_created',)

    # @classmethod
    # def create_entry(cls, title, content, resources, time_spent, user):
    #     with DATABASE.transaction():
    #         try:
    #             cls.create(
    #                 title=title,
    #                 content=content,
    #                 resources=resources,
    #                 time_spent=time_spent,
    #                 user=user
    #             )
    #         except IntegrityError:
    #             raise ValueError("Entry already exists")
    #             entry_record = Entry.get(title=title)
    #             entry_record.content = content
    #             entry_record.resources = resoureces
    #             entry_record.time_spent = time_spent
    #             entry_record.save()



def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry, User], safe=True)
    DATABASE.close()
