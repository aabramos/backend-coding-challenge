# !/usr/bin/python
# -*- coding: utf-8 -*-

from database import db, mw


class Translation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_text = db.Column(db.String(255), nullable=False)
    translated_text = db.Column(db.String(255), nullable=False)
    uid = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(15), nullable=False)

    def __init__(self, source_text, translated_text, uid, status):
        self.source_text = source_text
        self.translated_text = translated_text
        self.uid = uid
        self.status = status


class TranslationSchema(mw.ModelSchema):
    class Meta:
        model = Translation
