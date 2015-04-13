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
    postparser.add_argument('is_panorama', type=bool, default=False)
    postparser.add_argument('photo', type=FileStorage, location='files',
                            required=True)

    @staticmethod
    def allowed_file(filename):
        allowed_exts = app.config['PHOTOS_ALLOWED_EXTENSIONS']
        return '.' in filename and filename.rsplit('.', 1)[1] in allowed_exts

    def get(self):
        args = self.getparser.parse_args()
        filter_args = []
        if args['since'] is not None:
            filter_args += [models.Photo.timestamp > args['since']]
        return [x.as_dict() for x in
                models.Photo.query.filter(*filter_args).all()]

    @staticmethod
    def upload_photo(f, timestamp, is_panorama):
        if not f or not Photos.allowed_file(f.filename):
            return {'message': "File extension is not allowed!"}, 400

        x = models.Photo(timestamp=timestamp, is_panorama=is_panorama)
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

    def post(self):
        args = self.postparser.parse_args()
        return self.upload_photo(args['photo'], args['timestamp'],
                                 args['is_panorama'])

    class Panorama(Resource):
        def get(self):
            panorama = (models.Photo.query
                        .filter_by(is_panorama=True)
                        .order_by(models.Photo.timestamp.desc()).first_or_404())
            return panorama.as_dict()

        def put(self):
            args = Photos.postparser.parse_args()
            return Photos.upload_photo(args['photo'], args['timestamp'], True)