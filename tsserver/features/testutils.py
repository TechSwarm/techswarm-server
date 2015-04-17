import os

from tsserver import db
from tsserver.dtutils import datetime_from_str


def resource_path():
    return os.path.join(os.path.dirname(__file__), 'resources')


def open_resource(name, *args, **kwargs):
    path = os.path.join(resource_path(), name)
    return open(path, *args, **kwargs)


def table_to_database(table, model):
    """
    Parse data in table, where each row represents one record in database,
    and add it to the database.

    For instance, calling this function with a table like this:

        | temperature | pressure |
        | 23.6        | 1000     |
        | 24.0        | 1100     |

    Will have basically the same effect as calling:

        db.session.add(model(temperature=23.6, pressure=1000))
        db.session.add(model(temperature=24.0, pressure=1100))
        db.session.commit()

    Please note that each row is parsed using :function:`parse_data_table_row`,
    so values of columns like timestamp will be parsed properly.

    :param table: context.table object
    :type table: behave.model.Table
    :param model: model to create objects of
    :type model: db.model
    :return: None
    """
    for row in table:
        d = parse_data_table_row(row)
        x = model(**d)
        db.session.add(x)
    db.session.commit()


def parse_data_table_row(row):
    """
    Parse provided row and return dictionary containing data to be passed
    to model constructor

    :param row: row to parse
    :type row: behave.model.Row
    :return: dictionary of parsed data
    """

    def parse_val(x, y):
        if x == 'timestamp':
            return datetime_from_str(y)
        return y

    return dict((x, parse_val(x, y)) for x, y in row.as_dict().items())
