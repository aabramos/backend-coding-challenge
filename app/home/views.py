# !/usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template, make_response,\
    request, redirect, url_for
from flask_restful import Resource
from app.home.forms import UnbabelForm
from app import socketio
from config import Config


class Index(Resource):
    """
    Views using flask_restful Api.
    """
    def get(self):
        headers = {'Content-Type': 'text/html'}
        form = UnbabelForm()
        return make_response(
            render_template('index.html', title='Unbabel Coding Challenge', form=form, async_mode=socketio.async_mode),
            200,
            headers,
        )

    def post(self):
        input_text = request.form.get('input_field')

        # Avoiding circular imports
        from app.tasks import send_request
        # Send translation request on post
        send_request.delay(input_text, Config.SOURCE_LANGUAGE, Config.TARGET_LANGUAGE,)

        return redirect(url_for('index'))
