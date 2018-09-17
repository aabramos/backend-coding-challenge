import requests
from flask import flash
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
    #response = requests.post(Config.UNBABEL_SANDBOX_URL, json=payload, headers=Config.HEADERS)
    if response:
        save_request.delay(response)
    else:
        flash('Error')
        

@celery.task
def save_request(data):
    translation = Translation(
        source_text=data.text,
        translated_text='-',
        uid=data.uid,
        status='requested',
    )
    db.session.add(translation)
    db.session.commit()


@celery.task
def get_periodic_request():
    translations = Translation.query.all()

    if translations:
        for translation in translations:
            #tr_check_url = Config.UNBABEL_SANDBOX_URL + translation.uid

            data = api.get_translation(translation.uid)

            #data = requests.get(tr_check_url, headers=Config.HEADERS)
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
