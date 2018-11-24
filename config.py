import os
import random
import string

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    # SECRET_KEY = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    SECRET_KEY = os.environ.get('SECRET_KEY')



class ProductionConfig(Config):
    DEBUG = False
    # DATABASE_URL =  os.environ.get('PRODUCTION_DATABASE_URL')



class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    # DATABASE_URL =  os.environ.get('DEVELOPMENT_URL')

class TestingConfig(Config):
    TESTING = True
    # DATABASE_URL =  os.environ.get('TESTING_URL')


app_config = {
    "TESTING": TestingConfig,
    "DEVELOPMENT": DevelopmentConfig,
    "PRODUCTION": ProductionConfig

}
