from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import Api


app = Flask(__name__, static_folder='../files')
app.config.from_object('config')
db = SQLAlchemy(app)
api = Api(app, catch_all_404s=True)

# A few improvements to Flask-RESTful JSON serializer
from tsserver import jsonencoder

# Otherwise we're going to receive messages like
# "You have requested this URI [/panorama] but did you mean /panorama ?"
app.config['ERROR_404_HELP'] = False

from tsserver import actions
