#instance/config.py
"""
    This module holds api configuration.
"""
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
        Parent configuration class.
    """
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    TESTING = False
    JWT_ALGORITHM = 'HS256'
    JWT_SECRET_KEY = 'jtw-very-supa-secret'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']


class DevelopmentConfig(Config):
    """
        Development configuration class.
    """
    DEBUG = True


class TestingConfig(Config):
    """
        Testing configuration class.
    """
    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    """
        Production configuratio class.
    """
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
