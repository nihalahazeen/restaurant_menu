import os


class Config(object):
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class LocalConfig(Config):
    SQLALCHEMY_ECHO = False
    ENVIRONMENT = os.environ.get("ENVIRONMENT")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
