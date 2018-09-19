# !/usr/bin/python
# -*- coding: utf-8 -*-

import app
import os
from database import db
from app.home.models import Translation

app = app.create_app(os.getenv("FLASK_ENV"))


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Translation': Translation, }
