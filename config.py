class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'hj67gyu_;,,../ku9inm'


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
