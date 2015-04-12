from tsserver import api
from tsserver.photos.api import Photos
from tsserver.telemetry.api import Telemetry


api.add_resource(Telemetry, '/telemetry')
api.add_resource(Photos, '/photos')
