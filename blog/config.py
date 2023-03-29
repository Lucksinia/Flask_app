import os
from dotenv import load_dotenv


load_dotenv()
DEBUG = False
TESTING = False
# SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
SQLALCHEMY_DATABASE_URI = 'sqlite:///blog.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "gsufioedo[ad128946]"
WTF_CSRF_SECRET_KEY="gsufioedo[ad128946]"
WTF_CSRF_ENABLED = True
FLASK_ADMIN_SWATCH = 'cosmo'
SOCIAL_AUTH_USER_MODEL = 'blog.models.User'

OPENAPI_URL_PREFIX = '/api/swagger'
OPENAPI_SWAGGER_UI_PATH = '/'
OPENAPI_SWAGGER_UI_VERSION = '3.22.0'

class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "abcdefg123456"
    WTF_CSRF_ENABLED = True


class DevConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")


class TestingConfig(BaseConfig):
    TESTING = True