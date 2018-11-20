from flask import Flask

from config import app_config

from app.views.users import users_bp


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])

    app.register_blueprint(users_bp)
    
    return app
