from flask import Flask
from .web import main
from .utils import make_celery
from . import config


def create_app(config=config):
    app = Flask(__name__)
    app.config.from_object(config)
    celery = make_celery(app)
    celery.set_default()

    app.register_blueprint(main)
    
    return app, celery