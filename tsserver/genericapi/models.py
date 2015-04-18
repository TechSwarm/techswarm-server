from tsserver import db
from tsserver.model import Model


class Telemetry(Model):
    """
    All the data that is going to be obtained in regular time intervals
    (every second or so).
    """

    timestamp = db.Column(db.DateTime, primary_key=True)
    temperature = db.Column(db.Float)
    """Temperature in Celsius."""
    pressure = db.Column(db.Float)
    """Air pressure in hPa."""


class Status(Model):
    timestamp = db.Column(db.DateTime, primary_key=True)
    phase = db.Column(db.Enum('disconnected', 'launch_preparation',
                              'countdown', 'launch', 'descend',
                              'ground_operations', 'mission_complete'))
