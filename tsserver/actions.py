from tsserver import api
from tsserver.bulk.api import Bulk
from tsserver.genericapi import CollectionGenericAPI, CurrentElementGenericAPI
from tsserver.photos.api import Photos
from tsserver.genericapi.models import Telemetry, Status


bulk = Bulk(api)

# Status
bulk.add_resource(CollectionGenericAPI.create(Status), '/status')
api.add_resource(CurrentElementGenericAPI.create(Status), '/status/current')

# Photos
api.add_resource(Photos, '/photos')
api.add_resource(Photos.Panorama, '/panorama')

# Other
bulk.add_resource(CollectionGenericAPI.create(Telemetry), '/telemetry')
