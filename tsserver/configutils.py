import os

from tsserver import app


def get_upload_dir():
    return os.path.join(app.root_path, app.config['PHOTOS_UPLOAD_FOLDER'])
