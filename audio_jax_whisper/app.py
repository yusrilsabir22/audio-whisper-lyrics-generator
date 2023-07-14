from flask import Flask
from .web import main
from .utils import make_celery
from celery import Celery


def create_app():
    app = Flask(__name__)
    
    app.config["CELERY_CONFIG"] = {"broker_url": "redis://localhost:6379", "result_backend": "redis://localhost:6379"}

    celery = make_celery(app)
    celery.set_default()

    app.register_blueprint(main)
    
    return app, celery