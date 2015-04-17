from flask.ext.restful import Resource, reqparse
from sqlalchemy.sql import sqltypes

from tsserver import db
from tsserver.dtutils import timestamp


class GenericAPI(Resource):
    """
    Base class for "Generic API" classes whose purpose is to automagically
    create an API out of provided model that allows to retrieve and add data.
    Generic API classes should be used whenever an API for simple model is
    needed.
    """

    _model = None
    """The model to use to create API of."""

    get_parser = reqparse.RequestParser()
    get_parser.add_argument('since', type=timestamp)

    @classmethod
    def create(cls, model, name=None):
        """
        Create new GenericAPI class for the model provided. Can be used with
        `Api.add_resource()` like:

            api.add_resource(WhateverGenericAPI.create(Model), '/url')

        :param model: model to create API of
        :type model: db.Model
        :param name: name for the class that's going to be created. Defaults
            to `model.__name__`
        :type name: str
        :rtype: type
        """
        if name is None:
            name = model.__name__
        return type(name, (cls,), {'_model': model})

    def __init__(self):
        self._post_parser = None
        super().__init__()

    def _create_element(self):
        """
        Parse arguments from post_parser and create new element out of it.

        :return: created model instance
        """
        args = self.post_parser.parse_args()
        x = self._model(**args)
        db.session.add(x)
        db.session.commit()
        return x

    @property
    def post_parser(self):
        """
        :class:`.RequestParser` to be used with POST/PUT. Should parse all the
        arguments needed to create new instance of a model.

        :rtype: RequestParser
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
        parser.add_argument(column.description, required=True,
                            **self._get_column_args(column))

    def _get_column_args(self, column):
        """
        Return dict containing kwargs for add_argument method of
        RequestParser for the column provided

        :type column: sqlalchemy.sql.schema.Column
        :rtype: dict
        """
        col_type = type(column.type)
        args = {'type': (self.arg_types[col_type] if col_type in self.arg_types
                         else column.type.python_type)}
        if col_type == sqltypes.Enum:
            args['choices'] = column.type.enums

        return args

    arg_types = {sqltypes.DateTime: timestamp,
                 sqltypes.Enum: str}
    """Dictionary that maps some kind of special SQL column types into Python
    equivalents. If mapping for column type is not available in this
    dictionary, `column.type.python_type` is used."""


class CollectionGenericAPI(GenericAPI):
    """
    Generic API class that provides GET method, which retrieves list of
    elements of model given, and POST method, which allows to add new element.
    """

    def get(self):
        args = self.get_parser.parse_args()
        filter_args = []
        if args['since'] is not None:
            filter_args += [self._model.timestamp > args['since']]
        return [x.as_dict() for x in
                self._model.query.filter(*filter_args).all()]

    def post(self):
        return self._create_element().as_dict(), 201


class LatestElementGenericAPI(GenericAPI):
    """
    Generic API class that provides GET method, which retrieves the element
    with latest timestamp in model given, and PUT method, which allows to add
    new element (which actually replaces the current one if new timestamp is
    greater than the old one).
    """

    @classmethod
    def create(cls, model, name=None):
        if name is None:
            name = model.__name__ + '-latest'
        return super(LatestElementGenericAPI, cls).create(model, name)

    def get(self):
        return (self._model.query.order_by(self._model.timestamp.desc())
                .first_or_404()).as_dict()

    def put(self):
        return self._create_element().as_dict(), 201
