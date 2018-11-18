from collections import OrderedDict

import yaml
from peewee import SqliteDatabase, chunked

from .models import Hotel, db_proxy


def dict_representer(dumper, data):
    return dumper.represent_dict(data.items())

yaml.Dumper.add_representer(OrderedDict, dict_representer)


def yaml_format(items, filepath):
    with filepath.open('w+', encoding='utf-8') as f:
        yaml.dump(items, f, Dumper=yaml.Dumper, default_flow_style=False)


def sqlite_format(items, filepath):
    db = SqliteDatabase(filepath.as_posix())
    db_proxy.initialize(db)
    db.create_tables((Hotel,))

    with db.atomic():
        Hotel.delete().execute()
        for batch in chunked(items, 900):
            Hotel.insert_many(batch).execute()
