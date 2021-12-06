import logging
import os
from flask import Flask
from flask_mongoengine import MongoEngine
from redis import Redis
import rq
from config import Config

db = MongoEngine()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app

from app import models, json_formatters, classifiers
