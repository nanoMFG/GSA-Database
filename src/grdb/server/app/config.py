from os import environ, path
from dotenv import load_dotenv

base_dir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(base_dir, '../.env'), override=True)


class Config:
    """
    Config class that will be used for flask app config.
    Store .env file in "src/grdb/server" folder
    """
    DB_HOST = environ.get('DB_HOST')

    DEV_URL = environ.get('DEV_URL')
    DEV_ADMIN_USER = environ.get('DEV_ADMIN_USER')
    DEV_ADMIN_PASS = environ.get('DEV_ADMIN_PASS')
    DEV_WRITE_USER = environ.get('DEV_WRITE_USER')
    DEV_WRITE_PASS = environ.get('DEV_WRITE_PASS')
    DEV_READ_USER = environ.get('DEV_READ_USER')
    DEV_READ_PASS = environ.get('DEV_READ_PASS')

    TEST_URL = environ.get('TEST_URL')
    TEST_ADMIN_USER = environ.get('TEST_ADMIN_USER')
    TEST_ADMIN_PASS = environ.get('TEST_ADMIN_PASS')
    TEST_WRITE_USER = environ.get('TEST_WRITE_USER')
    TEST_WRITE_PASS = environ.get('TEST_WRITE_PASS')
    TEST_READ_USER = environ.get('TEST_READ_USER')
    TEST_READ_PASS = environ.get('TEST_READ_PASS')

    PROD_URL = environ.get('PROD_URL')
    PROD_ADMIN_USER = environ.get('PROD_ADMIN_USER')
    PROD_ADMIN_PASS = environ.get('PROD_ADMIN_PASS')
    PROD_WRITE_USER = environ.get('PROD_WRITE_USER')
    PROD_WRITE_PASS = environ.get('PROD_WRITE_PASS')
    PROD_READ_USER = environ.get('PROD_READ_USER')
    PROD_READ_PASS = environ.get('PROD_READ_PASS')

    DEV_DATABASE_URL = environ.get('DEV_DATABASE_URL')
    DEV_DATABASE_ARGS = environ.get('DEV_DATABASE_ARGS')
    DEV_DATABASE_URL_READ = environ.get('DEV_DATABASE_URL_READ')
    DEV_DATABASE_URL_WRITE = environ.get('DEV_DATABASE_URL_WRITE')
    DEV_DATABASE_URL_ADMIN = environ.get('DEV_DATABASE_URL_ADMIN')

    TEST_DATABASE_URL = environ.get('TEST_DATABASE_URL')
    TEST_DATABASE_ARGS = environ.get('TEST_DATABASE_ARGS')
    TEST_DATABASE_URL_READ = environ.get('TEST_DATABASE_URL_READ')
    TEST_DATABASE_URL_WRITE = environ.get('TEST_DATABASE_URL_WRITE')
    TEST_DATABASE_URL_ADMIN = environ.get('TEST_DATABASE_URL_ADMIN')

    PROD_DATABASE_URL = environ.get('PROD_DATABASE_URL')
    PROD_DATABASE_ARGS = environ.get('PROD_DATABASE_ARGS')
    PROD_DATABASE_URL_READ = environ.get('PROD_DATABASE_URL_READ')
    PROD_DATABASE_URL_WRITE = environ.get('PROD_DATABASE_URL_WRITE')
    PROD_DATABASE_URL_ADMIN = environ.get('PROD_DATABASE_URL_ADMIN')

    JWT_SECRET = environ.get('JWT_SECRET')
    AWS_S3_ACCESS_KEY_ID = environ.get('AWS_S3_ACCESS_KEY_ID')
    AWS_S3_SECRET_ACCESS_KEY = environ.get('AWS_S3_SECRET_ACCESS_KEY')
    AWS_S3_REGION_NAME = environ.get('AWS_S3_REGION_NAME')
    AWS_S3_BUCKET_NAME = environ.get('AWS_S3_BUCKET_NAME')