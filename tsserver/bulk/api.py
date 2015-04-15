from flask.ext.restful import Resource, abort


class Bulk:
    """
    A class that provides support for bulk retrieving and adding data (in one
    request).
    """

    actions = {}
    """List of resources available for bulk actions"""

    def __init__(self, api):
        """
        :type api: flask.ext.restful.Api
        """
        self.api = api
        self.BulkActions.actions = self.actions

        # A resource added twice with different URLs and methods should work
        # perfectly fine, but unfortunately Flask-RESTful calls as_view()
        # internally in add_resource, which results in exception indicating
        # that two different view function are going to be added as the same
        # endpoint - that's why the endpoints here are different.
        api.add_resource(self.BulkActions, '/bulk/<string:resources>',
                         endpoint='bulk-get', methods=['GET', ])
        api.add_resource(self.BulkActions, '/bulk/', endpoint='bulk-post',
                         methods=['POST', ])

    def add_resource(self, resource, url, name=None):
        """
        Add resource both to API and Bulk actions.

        :param resource: resource to add
        :type resource: Resource
        :param url: URL for the resource
        :type url: str
        :param name: Used as resource endpoint and name used to retrieve it
            via /bulk/<name>. Defaults to `resource.__name__.lower()`
        :type name: str
        """
        if name is None:
            name = resource.__name__.lower()
        self.api.add_resource(resource, url, endpoint=name)
        self.actions[name] = resource

    class BulkActions(Resource):
        def get(self, resources):
            """
            :param resources: Comma-separated list of resources to get
            :type resources: str
            """
            response = {}
            for name in resources.split(','):
                if name in self.actions:
                    response[name] = self.actions[name]().get()
                else:
                    abort(404)
            return response

        def post(self):
            abort(404)
