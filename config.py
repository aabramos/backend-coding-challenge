# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv
load_dotenv()


class Config(object):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.environ.get("SECRET_KEY")
    HOME_URL = 'localhost'
    SOURCE_LANGUAGE = 'en'
    TARGET_LANGUAGE = 'es'

    POSTGRES = {
        'user': os.environ.get("POSTGRES_USER"),
        'pw': os.environ.get("POSTGRES_PW"),
        'db': os.environ.get("POSTGRES_DB"),
        'host': os.environ.get("POSTGRES_HOST"),
        'port': os.environ.get("POSTGRES_PORT"),
    }
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis
    LISTEN = ['default']
    REDISTOGO_URL = os.environ.get("POSTGRES_HOST") or 'redis://localhost:6379'

    # To start celery worker and beater:
    # celery -A app.tasks worker -B --loglevel=info
    CELERYBEAT_SCHEDULE = {
        'runs-every-15-seconds': {
            'task': 'app.tasks.get_periodic_request',
            'schedule': 15.0,
        }
    }

    # Unbabel API
    UNBABEL_SANDBOX_USERNAME = os.environ.get("SANDBOX_USERNAME")
    UNBABEL_SANDBOX_KEY = os.environ.get("SANDBOX_KEY")
    UNBABEL_SANDBOX_URL = 'https://sandbox.unbabel.com/tapi/v2/translation/'
