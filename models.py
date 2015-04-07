from datetime import datetime
from tsserver import db


class Telemetry(db.Model):
    """
    All the data that is going to be obtained in regular time intervals
    (every second or so).
    """

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    temperature = db.Column(db.Float)
    pressure = db.Column(db.Float)

    def __init__(self, temperature, pressure, timestamp=datetime.now()):
        self.timestamp = timestamp
        self.temperature = temperature
        self.pressure = pressure

    def as_dict(self):
        return {'temperature': self.temperature,
                'pressure': self.pressure}
