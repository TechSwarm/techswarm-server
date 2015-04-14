from tsserver import api
from tsserver.genericapi import CollectionGenericAPI
from tsserver.photos.api import Photos
from tsserver.genericapi.models import Telemetry


api.add_resource(CollectionGenericAPI.create(Telemetry), '/telemetry')
api.add_resource(Photos, '/photos')
api.add_resource(Photos.Panorama, '/panorama')
