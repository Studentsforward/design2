from authomatic.providers import oauth2
import os
basedir = os.path.abspath(os.path.dirname(__file__))

AUTHOMATIC_CONFIG = {
    'fb': {
        'id': 1,
        'class_': oauth2.Facebook,
        'consumer_key': '393753284298131',
        'consumer_secret': '2977f7d4fde1ffa8a4a7990c5b27cecf',
        'scope': ['user_about_me', 'email']
    }
}

class Config(object):
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///mydb.db'

    def init_app(app):
        pass

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
