# !/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import Api
from flask_wtf.csrf import CSRFProtect
from celery import Celery
from flask_socketio import SocketIO
from config import Config
from database import database_init


CELERY_TASK_LIST = [
    'app.tasks'
]
socketio = SocketIO()


def make_celery(app=None):
    app = app or create_app()
    celery = Celery(app.import_name,
                    broker=Config.REDISTOGO_URL,
                    include=CELERY_TASK_LIST,
                    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app(config_class=Config):
    app = Flask(__name__)
    api = Api(app)
    csrf = CSRFProtect()

    app.config.from_object(config_class)
    database_init(app)
    socketio.init_app(app)
    csrf.init_app(app)

    from app.home.views import Index
    api.add_resource(Index, '/')

    return app


@socketio.on('client_connected')
def handle_client_connect_event(json):
    print('received json: {0}'.format(str(json)))


__version_info__ = '1.0'
__author__ = 'Adriano Alberto Borges Ramos'
__email__ = 'adriano@teacherivy.com'
