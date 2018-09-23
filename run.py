# !/usr/bin/python
# -*- coding: utf-8 -*-

import app
from database import db
from app.home.models import Translation

app = app.create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Translation': Translation, }


if __name__ == '__main__':
    app.run()
