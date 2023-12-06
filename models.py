from peewee import *

# db = SqliteDatabase('data.db')
db = MySQLDatabase(database='cuvix', user='root', host='localhost')

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
db.connect()
db.create_tables([User, Post])
