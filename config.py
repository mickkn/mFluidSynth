import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ZJpoasj187321+07!Jidaspj'

    STATIC_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app', 'static')
