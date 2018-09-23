# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv
load_dotenv()


class Config(object):
    DEBUG = True
    TESTING = False
    WTF_CSRF_ENABLED = True
    USE_RELOADER = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    HOME_URL = 'localhost'
    SOURCE_LANGUAGE = 'en'
    TARGET_LANGUAGE = 'es'

    # SQLAlchemy
    POSTGRES = {
        'user': os.environ.get("POSTGRES_USER"),
        'pw': os.environ.get("POSTGRES_PW"),
        'db': os.environ.get("POSTGRES_DB"),
        'host': os.environ.get("POSTGRES_HOST"),
        'port': os.environ.get("POSTGRES_PORT"),
    }
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis
    LISTEN = ['default']
    REDISTOGO_URL = os.environ.get("REDISTOGO_URL") or 'redis://localhost:6379'

    # Celery
    CELERYBEAT_SCHEDULE = {
        'runs-every-30-seconds': {
            'task': 'app.tasks.get_periodic_request',
            'schedule': 30.0,
        }
    }
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND") or 'redis://localhost:6379'

    # Unbabel API
    UNBABEL_SANDBOX_USERNAME = os.environ.get("SANDBOX_USERNAME")
    UNBABEL_SANDBOX_KEY = os.environ.get("SANDBOX_KEY")
    UNBABEL_SANDBOX_URL = 'https://sandbox.unbabel.com/tapi/v2/translation/'


class TestConfig(Config):
    TESTING = True
    DEBUG = False
    WTF_CSRF_ENABLED = False
    CELERY_ALWAYS_EAGER = True

    POSTGRES = {
        'user': os.environ.get("POSTGRES_USER_TEST"),
        'pw': os.environ.get("POSTGRES_PW_TEST"),
        'db': os.environ.get("POSTGRES_DB_TEST"),
        'host': os.environ.get("POSTGRES_HOST_TEST"),
        'port': os.environ.get("POSTGRES_PORT_TEST"),
    }
