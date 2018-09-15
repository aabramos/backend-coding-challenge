import requests
from app import make_celery
from app.models import Translation
from database import db
from config import Config

celery = make_celery()


@celery.task
def send_text(source_text):
    payload = {
        'text': source_text,
        'source_language': 'en',
        'target_language': 'es',
        'text_format': 'text',
    }
    response = requests.post(Config.URL, json=payload, headers=Config.HEADERS)
    if response.status_code == 201:
        data = response.json()
        save_data.delay(data)


@celery.task
def save_data(data):
    translation = Translation(
        source_text=data['text'],
        translated_text='Pending',
        uid=data['uid'],
        status=data['status'],
    )
    db.session.add(translation)
    db.session.commit()
