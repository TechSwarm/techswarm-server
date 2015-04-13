from flask import url_for

from tsserver import db
from tsserver.dtutils import datetime_to_str


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    filename = db.Column(db.String(200))
    is_panorama = db.Column(db.Boolean, default=False)

    def as_dict(self):
        return {'id': self.id,
                'timestamp': datetime_to_str(self.timestamp),
                'isPanorama': self.is_panorama,
                'filename': self.filename,
                'url': url_for('static', filename=self.filename)}
