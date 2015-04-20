from datetime import datetime
from decimal import Decimal
from flask.ext.restful.representations import json
from json import JSONEncoder
from tsserver.dtutils import datetime_to_str


class TSEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return datetime_to_str(o)
        elif isinstance(o, Decimal):
            return float(o)
        return super(TSEncoder, self).default(o)


json.settings['cls'] = TSEncoder
