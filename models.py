from peewee import *

db = None
try:
    db = MySQLDatabase(database='cuvix', user='root', host='localhost')
    db.connect()
except:
    db = SqliteDatabase('data.sqlite')


class User(Model):
    username = CharField(max_length=64, primary_key=True)
    password = TextField()
    created_at = DateTimeField()

    class Meta:
        database = db


class Post(Model):
    content = TextField()
    created_at = DateTimeField()
    posted_by = ForeignKeyField(User)

    class Meta:
        database = db

# User.password.key = key_derivation_fn
db.create_tables([User, Post])
