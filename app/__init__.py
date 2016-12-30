from flask import Flask, render_template, request, redirect, url_for, make_response, abort
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy

from config import config, AUTHOMATIC_CONFIG
from plaid import Client
import os

from .models import db, User, Connection
from authomatic import Authomatic

import logging
from logging.handlers import RotatingFileHandler
import facebook


login_manager = LoginManager()
login_manager.login_view = "login"

handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.NOTSET)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    app.logger.addHandler(handler)

    db.init_app(app)
    with app.app_context():
        db.create_all()
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
