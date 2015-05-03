from tsserver import api
from tsserver.bulk.api import Bulk
from tsserver.genericapi import CollectionGenericAPI, CurrentElementGenericAPI
from tsserver.photos.api import Photos
from tsserver.genericapi.models import (
    Status, GroundStationInfo, IMU, SHT, GPS, PlanetaryData
)

bulk = Bulk(api)

# Status
bulk.add_resource(CollectionGenericAPI.create(Status), '/status')
api.add_resource(CurrentElementGenericAPI.create(Status), '/status/current')

# Ground station info
bulk.add_resource(CollectionGenericAPI.create(GroundStationInfo, 'gsinfo'),
                  '/gsinfo')
api.add_resource(CurrentElementGenericAPI.create(GroundStationInfo),
                 '/gsinfo/current', endpoint='gsinfo-current')

# Photos
bulk.add_resource(Photos, '/photos')
api.add_resource(Photos.Panorama, '/panorama')

# Other
bulk.add_resource(CollectionGenericAPI.create(IMU), '/imu')
bulk.add_resource(CollectionGenericAPI.create(SHT), '/sht')
bulk.add_resource(CollectionGenericAPI.create(GPS, arguments_required=False),
                  '/gps')
bulk.add_resource(
    CollectionGenericAPI.create(PlanetaryData, arguments_required=False,
                                defaults_to_last=True), '/planetarydata')
