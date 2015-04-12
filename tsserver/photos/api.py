import os

from flask.ext.restful import Resource, reqparse
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from tsserver import app, db, configutils
from tsserver.dtutils import timestamp
from tsserver.photos import models


class Photos(Resource):
    getparser = reqparse.RequestParser()
    getparser.add_argument('since', type=timestamp)

    postparser = reqparse.RequestParser()
    postparser.add_argument('timestamp', type=timestamp, required=True)
    postparser.add_argument('photo', type=FileStorage, location='files',
                            required=True)

    def allowed_file(self, filename):
        allowed_exts = app.config['PHOTOS_ALLOWED_EXTENSIONS']
        return '.' in filename and filename.rsplit('.', 1)[1] in allowed_exts

    def get(self):
        args = self.getparser.parse_args()
        filter_args = []
        if args['since'] is not None:
            filter_args += [models.Photo.timestamp > args['since']]
        return [x.as_dict() for x in
                models.Photo.query.filter(*filter_args).all()]

    def post(self):
        args = self.postparser.parse_args()
        f = args['photo']
        if not f or not self.allowed_file(f.filename):
            return {'error': "File extension is not allowed!"}, 400

        x = models.Photo(timestamp=args['timestamp'])
        db.session.add(x)
        db.session.commit()

        # ID in database is prepended to the filename to avoid multiple images
        # with the same filenames
        filename = '%.3d_%s' % (x.id,
                                secure_filename(os.path.basename(f.filename)))
        f.save(os.path.join(configutils.get_upload_dir(), filename))

        x.filename = filename
        db.session.commit()
        return x.as_dict(), 201
