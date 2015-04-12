from flask import url_for
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


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    filename = db.Column(db.String(200))

    def as_dict(self):
        return {'id': self.id,
                'timestamp': datetime_to_str(self.timestamp),
                'filename': self.filename,
                'url': url_for('static', filename=self.filename)}
