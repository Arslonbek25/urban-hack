
import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SECRET_KEY = os.environ.get("SECRET_KEY")
