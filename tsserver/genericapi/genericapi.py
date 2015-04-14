from flask.ext.restful import Resource, reqparse
from sqlalchemy.sql import sqltypes

from tsserver import db
from tsserver.dtutils import timestamp


class CollectionGenericAPI(Resource):
    """
    Class that takes a model and automagically creates an API out
    of it that provides GET (retrieve elements) and POST method (add new entry).
    Should be used whenever an API for simple model is needed.
    """

    _model = None
    """The model to use to create API of."""

    getparser = reqparse.RequestParser()
    getparser.add_argument('since', type=timestamp)

    @staticmethod
    def create(model):
        """
        Create new CollectionGenericAPI class for the model provided. Can be
        used with `Api.add_resource()` like:

            api.add_resource(CollectionGenericAPI.create(Model), '/url')

        :param model: model to create API of
        :type model: db.Model
        :rtype: CollectionGenericAPI
        """

        class API(CollectionGenericAPI):
            _model = model

        # endpoint name is taken from __name__ by default, so set new value
        # to avoid conflicts
        API.__name__ = model.__name__
        return API

    def __init__(self):
        self._post_parser = None
        super().__init__()

    def get(self):
        args = self.getparser.parse_args()
        filter_args = []
        if args['since'] is not None:
            filter_args += [self._model.timestamp > args['since']]
        return [x.as_dict() for x in
                self._model.query.filter(*filter_args).all()]

    def post(self):
        args = self.post_parser.parse_args()
        x = self._model(**args)
        db.session.add(x)
        db.session.commit()
        return x.as_dict(), 201

    @property
    def post_parser(self):
        """
        :class:`.RequestParser` to use with POST. Should parse all the
        arguments needed to create new instance of a model.
        :return:
        """
        if self._post_parser is not None:
            return self._post_parser
        self._post_parser = self.create_post_parser()
        return self._post_parser

    def create_post_parser(self):
        """
        Create :class:`.RequestParser` to use with POST out of column in model.

        :rtype: reqparse.RequestParser
        """
        post_parser = reqparse.RequestParser()
        for column in self._model.__table__.columns:
            self._parse_column(post_parser, column)
        return post_parser

    def _parse_column(self, parser, column):
        """
        Add argument to parser that will provide data needed to fill the
        column provided.

        :param parser: reqparse.RequestParser to add the argument to
        :type parser: reqparse.RequestParser
        :param column: The column to parse
        :type column: sqlalchemy.sql.schema.Column
        :return: None
        """
        col_type = self._get_column_type(column)
        if col_type is None:
            raise ValueError('Column type "%s" is not recognized!' %
                             column.type)
        parser.add_argument(column.description, type=col_type, required=True)

    def _get_column_type(self, column):
        """
        Return value type or the column

        :type column: sqlalchemy.sql.schema.Column
        :return: type
        """
        col_type = type(column.type)
        if col_type == sqltypes.DateTime:
            return timestamp
        elif col_type == sqltypes.Float:
            return float
