# Please note that relative paths are relative to 'app root' directory,
# i.e. tsserver/, not the one with runserver.py

# URL Format: dialect+driver://username:password@host:port/database
# SQLite:     sqlite://<nohostname>/<path>
# See: http://docs.sqlalchemy.org/en/latest/core/engines.html
SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'

# The folder where uploaded images should be put into. Remember that on
# production files from inside there should be served by web server on
# static files URL (by default /files, see initialization of Flask class in
# tsserver/__init__.py for that)
PHOTOS_UPLOAD_FOLDER = '../files'

# Allowed extensions for photos
PHOTOS_ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

# User credentials required to add data
USERNAME = 'client'
# Remember to change this (preferably to long random string) on production!
PASSWORD = 'secret'
