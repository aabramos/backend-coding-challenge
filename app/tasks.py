# !/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import or_
from app import make_celery
from app.home.models import Translation
from unbabel.api import UnbabelApi
from database import db
from config import Config


celery = make_celery()
api = UnbabelApi(
    username=Config.UNBABEL_SANDBOX_USERNAME,
    api_key=Config.UNBABEL_SANDBOX_KEY,
    sandbox=True,
)


@celery.task
def send_request(source_text, source_language, target_language):
    """
    Translate a text using Unbabel API.

    :param source_text: Text submitted by the user.
    :param source_language: Original language.
    :param target_language: Target language.
    :return: The response text from Unbabel.
    """
    response = api.post_translations(
        text=source_text,
        target_language=target_language,
        source_language=source_language,
        callback_url=Config.HOME_URL,
    )
    if response:
        save_request.delay(response.uid, response.text)

    return response.text


@celery.task
def save_request(uid, text):
    """
    Saves the translation request on the database.

    :param uid: returned from Unbabel.
    :param text: Text submitted by the user.
    :return: None.
    """
    translation = Translation(
        source_text=text,
        translated_text='-',
        uid=uid,
        status='requested',
    )
    db.session.add(translation)
    db.session.commit()


@celery.task
def get_periodic_request():
    """
    Checks every 30 seconds with Unbabel if a translation is ready.
    :return: None.
    """
    translations = Translation.query.filter(or_(
        Translation.status == 'requested',
        Translation.status == 'pending',
    )).all()

    try:
        if translations:
            for translation in translations:
                data = api.get_translation(translation.uid)

                if data:
                    if data.status == 'completed':
                        update_request.delay(data.uid, 'translated', data.translation, )
                    elif data.status == 'translating':
                        update_request.delay(data.uid, 'pending')
    except api.UnauthorizedException:
        print('Please update the username and api key on the .env file.')


@celery.task
def update_request(uid, status, translated_text='-'):
    """
    Updates the translation.

    :param uid: returned from Unbabel.
    :param status: translation status.
    :param translated_text: returned from Unbabel.
    :return: None.
    """
    translation = Translation.query.filter_by(uid=uid).first()
    translation.status = status
    translation.translated_text = translated_text
    db.session.commit()
