from datetime import datetime
from tsserver import db
from tsserver.dtutils import datetime_to_str
from tsserver.strutils import to_camel_case


class Model(db.Model):
    """
    Base class for all models. What differs it from default Model class is
    serializable method, which is used to convert objects to JSON (or any other
    representation) more easily.
    """

    __abstract__ = True

    @property
    def serializable(self):
        """
        Return representation of the model that is JSON-serializable

        Basically what this function does is adding all columns with their
        values to one dictionary. Some value types (such as datetime) are
        beforehand converted to str to be JSON-serializable. Also, if model
        has 'resource_url' attribute, its value is added to dictionary as
        'url' key.

        Please note that this function converts all column names (i.e.
        dictionary keys) to camelCase. Reason for this behavior is while
        snake_case is Pythonic and used for naming columns in models,
        camelCase is more natural for JavaScript language, and therefore JSON.

        :rtype: dict
        """
        d = {}
        for column in self.__table__.columns:
            val = getattr(self, column.name)
            if isinstance(val, datetime):
                val = datetime_to_str(val)
            d[to_camel_case(column.name)] = val

        try:
            d['url'] = self.resource_url
        except AttributeError:
            pass

        return d
