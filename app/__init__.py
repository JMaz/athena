from gevent import monkey
monkey.patch_all()

import os, uuid
from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.socketio import SocketIO
from threading import Thread
from config import basedir

thread = None

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

salt = uuid.uuid4().hex
socketio = SocketIO(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'


if not app.debug:
	import logging
	from logging.handlers import RotatingFileHandler
	file_handler = RotatingFileHandler('tmp/athena.log', 'a', 1 * 1024 * 1024, 10)
	file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
	app.logger.setLevel(logging.INFO)
	file_handler.setLevel(logging.INFO)
	app.logger.addHandler(file_handler)
	app.logger.info('athena startup')

from app import views, models
