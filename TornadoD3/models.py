import peewee

myDB = peewee.MySQLDatabase("project_db", host="127.0.0.1", port=3306, user="root", passwd="",charset='utf8')


class MySQLModel(peewee.Model):
    """A base model that will use our MySQL database"""

    class Meta:
        database = myDB


class Admin(MySQLModel):
    id = peewee.PrimaryKeyField()
    name = peewee.CharField()
    user = peewee.CharField()
    password = peewee.CharField()


class User(MySQLModel):
    id = peewee.PrimaryKeyField()
    name = peewee.CharField()
    user = peewee.CharField()
    email = peewee.CharField()
    password = peewee.CharField()
    account = peewee.IntegerField()
    type = peewee.BooleanField()
    picture_address = peewee.CharField()
    status = peewee.IntegerField()
    User = peewee.ForeignKeyField('self')


class Payment(MySQLModel):
    id = peewee.PrimaryKeyField()
    amount = peewee.IntegerField()
    type = peewee.BooleanField()
    payer_id = peewee.IntegerField()
    date = peewee.DateField()
    User = peewee.ForeignKeyField(rel_model=User, to_field=User.id)


class Buy(MySQLModel):
    id = peewee.PrimaryKeyField()
    amount = peewee.IntegerField()
    concern = peewee.CharField()
    payer_id = peewee.IntegerField()
    date = peewee.DateField()
    per_share = peewee.IntegerField()


class Note(MySQLModel):
    id = peewee.PrimaryKeyField()
    date = peewee.DateField()
    title = peewee.CharField()
    text = peewee.CharField()
    User = peewee.ForeignKeyField(rel_model=User, to_field=User.id)


class Message(MySQLModel):
    id = peewee.PrimaryKeyField()
    id_reciver = peewee.IntegerField()
    description = peewee.CharField()
    date = peewee.DateField()
    date_buy = peewee.DateField()
    status = peewee.BooleanField()
    User = peewee.ForeignKeyField(rel_model=User, to_field=User.id)


class User_has_buy(MySQLModel):
    id = peewee.PrimaryKeyField()
    User = peewee.ForeignKeyField(rel_model=User, to_field=User.id)
    Buy = peewee.ForeignKeyField(rel_model=Buy, to_field=Buy.id)

