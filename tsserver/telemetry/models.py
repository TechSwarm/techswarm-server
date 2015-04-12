from tsserver import db
from tsserver.dtutils import datetime_to_str


class Telemetry(db.Model):
    """
    All the data that is going to be obtained in regular time intervals
    (every second or so).
    """

    timestamp = db.Column(db.DateTime, primary_key=True)
    temperature = db.Column(db.Float)
    """Temperature in Celsius."""
    pressure = db.Column(db.Float)
    """Air pressure in hPa."""

    def as_dict(self):
        return {'timestamp': datetime_to_str(self.timestamp),
                'temperature': self.temperature,
                'pressure': self.pressure}
