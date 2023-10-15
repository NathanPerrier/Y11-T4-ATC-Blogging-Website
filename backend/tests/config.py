from os.path import abspath, dirname, join
from backend.config import *

_cwd = dirname(abspath(__file__))


class BaseConfiguration(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = random.randbytes(32)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_ECHO = False
    HASH_ROUNDS = 100000


class TestConfiguration(BaseConfiguration):
    TESTING = True
    WTF_CSRF_ENABLED = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

    HASH_ROUNDS = 1


class DebugConfiguration(BaseConfiguration):
    DEBUG = True