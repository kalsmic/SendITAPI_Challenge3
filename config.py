import os

basedir = os.path.abspath(os.path.dirname(__file__))
import random
import string
class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    # DATABASE_URI = os.environ['DATABASE_URL']


class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URI = os.environ.get('DATABASE_URL_PRODUCTION  ')

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    DATABASE_URI = os.environ.get('TEST_DATABASE_URL')

class TestingConfig(Config):
    TESTING = True

app_config = {
    "TESTING": TestingConfig,
    "DEVELOPMENT": DevelopmentConfig,
    "PRODUCTION": ProductionConfig

}
