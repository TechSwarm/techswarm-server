from behave import *
from tsserver.features.testutils import table_to_database
from tsserver.genericapi.models import GroundStationInfo


@given("following ground station info")
def step_impl(context):
    table_to_database(context.table, GroundStationInfo)


@given("no ground station info in database")
def step_impl(context):
    GroundStationInfo.query.delete()
    assert GroundStationInfo.query.count() == 0
