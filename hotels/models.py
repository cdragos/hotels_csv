from peewee import CharField, IntegerField, Model, Proxy


db_proxy = Proxy()


class Hotel(Model):

    name = CharField()
    address = CharField()
    stars = IntegerField()
    contact = CharField()
    phone = CharField()
    uri = CharField()

    class Meta:
        database = db_proxy
