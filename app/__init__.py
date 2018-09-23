#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Lock
from celery import Celery
from flask import Flask, request, json
from flask_socketio import SocketIO, emit
from flask_restful import Api
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import func
from config import Config
from database import database_init
from app.home.models import Translation, TranslationSchema


async_mode = None

app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect(app)
api = Api(app)
database_init(app)
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

CELERY_TASK_LIST = [
    'app.tasks'
]

# Avoiding circular imports
from app.home.views import Index
api.add_resource(Index, '/')


def make_celery():
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


# The websocket is maintained in the background, and this
# function outputs a table for the client every second
def background_thread():
    with app.test_request_context():
        while True:
            socketio.sleep(2)
            translations = Translation.query.order_by(func.length(Translation.translated_text)).all()
            if translations:
                translations_schema = TranslationSchema(many=True)
                json_data = translations_schema.dump(translations).data
                formatted_data = json.dumps(json_data)
                socketio.emit('my_response', formatted_data, namespace='/test', json=True)


# This function is called when a web browser connects
@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})


# Notification that a client has disconnected
@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


# Run the web app
if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')


__version_info__ = '1.0'
__author__ = 'Adriano Alberto Borges Ramos'
__email__ = 'adriano@teacherivy.com'
