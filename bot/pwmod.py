from peewee import *

bd = PostgresqlDatabase(
    'bottest',  # Required by Peewee.
    user='bottest',  # Will be passed directly to psycopg2.
    password='03081998',  # Ditto.
    host='95.163.242.206')


class Users(bd.Model):
    chatid = CharField(max_length=200, unique=True)
    username = CharField(max_length=200, null=True)
    admin = BooleanField(default=False)
    stage = CharField(max_length=50, default='user')

    def changestageuser(self, stagename):
        self.stage = stagename
        self.save()


class Bots(bd.Model):
    name = TextField()
    category = CharField(null=True)
    token = TextField(null=True)
    url = TextField(null=True)
    user = ForeignKeyField(Users)
    pas = TextField(null=True)
    aktiv = BooleanField(default=True)
    process = BooleanField(default=False)


class Sests(bd.Model):
    name = CharField(max_length=50)
    set = TextField()
    bot = ForeignKeyField(Bots)


class Buts(bd.Model):
    name = CharField(max_length=200, null=True)
    text = TextField()
    link = TextField(null=True)
    chatid = TextField(null=True)
    bot = ForeignKeyField(Bots, default=10)


class SucessMsg(bd.Model):
    pinkod = CharField(max_length=200)
    msg = TextField(null=True)
    bot = ForeignKeyField(Bots)


class UsersBots(bd.Model):
    chatid = CharField(max_length=200)
    username = CharField(max_length=200, null=True)
    admin = BooleanField(default=False)
    stage = CharField(max_length=50, default='user')
    forsuc = CharField(null=True)
    bot = ForeignKeyField(Bots, default=10)
    limitbuts = IntegerField(default=4)
    limitpin = IntegerField(default=2)

    def changestageuser(self, stagename):
        self.stage = stagename
        self.save()
