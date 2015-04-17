from tsserver import api
from tsserver.bulk.api import Bulk
from tsserver.genericapi import CollectionGenericAPI, LatestElementGenericAPI
from tsserver.photos.api import Photos
from tsserver.genericapi.models import Telemetry, Status


bulk = Bulk(api)
bulk.add_resource(CollectionGenericAPI.create(Telemetry), '/telemetry')
bulk.add_resource(CollectionGenericAPI.create(Status), '/status')
bulk.add_resource(LatestElementGenericAPI.create(Status), '/status/current')

api.add_resource(Photos, '/photos')
api.add_resource(Photos.Panorama, '/panorama')
