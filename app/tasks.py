from flask import flash
from sqlalchemy import or_
from app import make_celery
from app.models import Translation
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
    response = api.post_translations(
        text=source_text,
        target_language=target_language,
        source_language=source_language,
        callback_url=Config.HOME_URL,
    )
    if response:
        save_request.delay(response.uid, response.text)
    else:
        flash('Error')
        

@celery.task
def save_request(uid, text):
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
    translations = Translation.query.filter(or_(
        Translation.status == 'requested',
        Translation.status == 'pending',
    )).all()

    if translations:
        for translation in translations:
            data = api.get_translation(translation.uid)

            if data:
                if data.status == 'completed':
                    update_request.delay(data.uid, 'translated', data.translation,)
                elif data.status == 'translating':
                    update_request.delay(data.uid, 'pending')


@celery.task
def update_request(uid, status, translated_text='-'):
    translation = Translation.query.filter_by(uid=uid).first()
    translation.status = status
    translation.translated_text = translated_text
    db.session.commit()
