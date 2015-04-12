import os

from tsserver.dtutils import datetime_from_str


def resource_path():
    return os.path.join(os.path.dirname(__file__), 'resources')


def open_resource(name, *args, **kwargs):
    path = os.path.join(resource_path(), name)
    return open(path, *args, **kwargs)


def parse_data_table_row(row):
    def parse_val(x, y):
        if x == 'timestamp':
            return datetime_from_str(y)
        return y

    return dict((x, parse_val(x, y)) for x, y in row.as_dict().items())
