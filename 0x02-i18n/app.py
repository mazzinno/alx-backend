#!/usr/bin/env python3

"""Route module for the API
"""

from typing import Union
from flask import Flask, render_template, request, g
from os import getenv

import pytz
from flask_babel import Babel
from pytz import timezone

app = Flask(__name__)
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """ Available languages class
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object('app.Config')


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> str:
    """ GET /
    Return:
        Hello world
    """
    return render_template('8-index.html')


@babel.localeselector
def get_locale() -> str:
    """ Determine best match for supported languages
    """
    locale = request.args.get("locale")
    if locale and locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user() -> Union[dict, None]:
    """ Returns a user dictionary or None
    """
    if request.args.get('login_as'):
        user = int(request.args.get('login_as'))
        if user in users:
            return users.get(user)
    else:
        return None


@app.before_request
def before_request():
    """ Executed before all other functions
    """
    g.user = get_user()


@babel.timezoneselector
def get_timezone():
    """ Infer approppriate timezone
    """
    try:
        time_zone = request.args.get('timezone')
        py_tz = pytz.timezone(time_zone)
    except pytz.exceptions.UnknownTimeZoneError:
        time_zone = 'UTC'
    return time_zone


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
