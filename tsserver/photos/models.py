from flask import url_for

from tsserver import db
from tsserver.model import Model


class Photo(Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    filename = db.Column(db.String(200))
    is_panorama = db.Column(db.Boolean, default=False)

    @property
    def resource_url(self):
        return url_for('static', filename=self.filename)
