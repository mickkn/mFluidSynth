import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask
from config import Config


def create_app(config_class=Config):

    app = Flask(__name__)

    app.config.from_object(config_class)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    if not app.debug:

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler(os.path.join('logs', 'msynth.log'), maxBytes=10240, backupCount=10)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('msynth startup')

    return app
