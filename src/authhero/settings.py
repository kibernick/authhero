import os


class Config:
    SECRET_KEY = os.environ.get("AUTHHERO_SECRET", "secret-key")
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    ENV = "development"
    DEBUG = True

    SQLALCHEMY_USER = "herouser"
    SQLALCHEMY_PASS = "heropass"
    SQLALCHEMY_HOST = "localhost"
    SQLALCHEMY_DB = "authhero"
    SQLALCHEMY_DATABASE_URI = "postgresql://{user}:{pwd}@{host}/{db}".format(
        user=SQLALCHEMY_USER,
        pwd=SQLALCHEMY_PASS,
        host=SQLALCHEMY_HOST,
        db=SQLALCHEMY_DB,
    )


class TestConfig(Config):
    ENV = "testing"
    DEBUG = True

    SQLALCHEMY_USER = "herouser_test"
    SQLALCHEMY_PASS = "heropass"
    SQLALCHEMY_HOST = "localhost"
    SQLALCHEMY_DB = "authhero_test"
    SQLALCHEMY_DATABASE_URI = "postgresql://{user}:{pwd}@{host}/{db}".format(
        user=SQLALCHEMY_USER,
        pwd=SQLALCHEMY_PASS,
        host=SQLALCHEMY_HOST,
        db=SQLALCHEMY_DB,
    )
