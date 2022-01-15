import os
from dotenv import load_dotenv

# load .env
dotenv_file = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_file)


class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY') or 'ThisIsJustATest'

    BUNDLE_ERRORS = True

    LOGGING_LEVEL = 'INFO'
    LOGGING_BACKUP_COUNT = 1
    LOGGING_FORMAT = '%(asctime)s - local.%(levelname)s - %(module)s ' \
                     '- %(funcName)s - %(message)s'

    INSTALLED_APPS = [
        'app',
    ]

    SQLALCHEMY_DATABASE_URI='mysql+pymysql://{}:{}@database/{}'.format(
        os.getenv('MYSQL_ROOT_USER'),
        os.getenv('MYSQL_ROOT_PASSWORD'),
        os.getenv('MYSQL_DATABASE')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    PROPAGATE_EXCEPTIONS=True


class TestingConfig(Config):
    TESTING = True


class LocalConfig(Config):
    DEBUG = True


class StagingConfig(Config):
    DEBUG = False

    LOGGING_FORMAT = '%(asctime)s - staging.%(levelname)s - %(funcName)s ' \
                     '- %(module)s - %(message)s'


class ProductionConfig(Config):
    DEBUG = False

    LOGGING_FORMAT = '%(asctime)s - production.%(levelname)s - %(funcName)s ' \
                     '- %(module)s - %(message)s'


config = {
    'local': LocalConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
