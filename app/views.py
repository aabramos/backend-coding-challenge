from flask import render_template, make_response,\
    request, redirect, url_for
from flask_restful import Resource
from sqlalchemy import func
from app.forms import UnbabelForm
from app.models import Translation
from config import Config


class Index(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        form = UnbabelForm()
        translations = Translation.query.filter(func.length(Translation.translated_text)).all()
        return make_response(
            render_template('index.html', title='Unbabel Coding Challenge', form=form, translations=translations,),
            200,
            headers,
        )

    def post(self):
        input_text = request.form.get('input_field')

        from app.tasks import send_request
        send_request.delay(input_text, Config.SOURCE_LANGUAGE, Config.TARGET_LANGUAGE,)

        return redirect(url_for('index'))
