import random
import string
class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))



class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URL ="dbname=sendit user=postgres password=postgres host=localhost"



class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    DATABASE_URL ="dbname=sendit user=postgres password=postgres host=localhost"



class TestingConfig(Config):
    TESTING = True
    DATABASE_URL ="dbname=sendit_TEST user=postgres password=postgres host=localhost"


app_config = {
    "TESTING": TestingConfig,
    "DEVELOPMENT": DevelopmentConfig,
    "PRODUCTION": ProductionConfig

}
