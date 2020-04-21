from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

""" Classes to handle being behind reverse proxy """


class ReverseProxied(object):
    def __init__(self, a):
        self.app = a

    def __call__(self, e, start_response):
        """ Checks for the existence of two headers: `HTTP_X_FORWARED_PREFIX`, and `HTTP_X_SCHEME`
        If found the contents of each header is prepended to the WSGI and flask base paths: <HTTP_X_SCHEME>://<HTTP_X_FORWARDED_PREFIX><flask route>

        This enables the flask/gunicorn combination to sit behind a reverse proxy without any special gunicorn configuration.
        Args:
            e (:obj:`FlaskEnvironment`): Flask Environment (passed by app)
            start_response (:obj:`FlaskResponse`): Flask response object (passed by app)

        Returns:
            e (:obj:`FlaskEnvironment`): Flask Environment modified by headers
            start_response (:obj:`FlaskResponse`): Flask response object

        """
        script_name = e.get('HTTP_X_FORWARDED_PREFIX', '')
        if script_name:
            e['SCRIPT_NAME'] = script_name
            path_info = e['PATH_INFO']
            if path_info.startswith(script_name):
                e['PATH_INFO'] = path_info[len(script_name):]

        scheme = e.get('HTTP_X_SCHEME', 'http')
        if scheme:
            e['wsgi.url_scheme'] = scheme
        return self.app(e, start_response)


""" create app instance """
app = Flask(__name__)

""" load app configuration """
app.config.from_object('config')

""" modify app __call__ to account for forwarded prefix header """
app.wsgi_app = ReverseProxied(app.wsgi_app)

""" create database session from app config """
db = SQLAlchemy(app, session_options={"autoflush": False})

""" create marshmallow instance from app config """
ma = Marshmallow(app)

""" Initialise cross origin resource sharing """
CORS(app)

""" if debugging is enabled, import debug toolbar and enable template auto reloading """
if app.debug:
    from flask_debugtoolbar import DebugToolbarExtension

    toolbar = DebugToolbarExtension(app)
    toolbar.init_app(app)
    app.TEMPLATES_AUTO_RELOAD = True

from app import models, controllers
