import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY')



class ProductionConfig(Config):
    DEBUG = False



class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True


app_config = {
    "TESTING": TestingConfig,
    "DEVELOPMENT": DevelopmentConfig,
    "PRODUCTION": ProductionConfig

}
