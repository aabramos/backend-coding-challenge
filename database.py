# !/usr/bin/python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
migrate = Migrate()
mw = Marshmallow()


def database_init(app):
    db.init_app(app)
    migrate.init_app(app, db)
    mw.init_app(app)
