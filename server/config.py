from os import environ, path
from dotenv import load_dotenv

base_dir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(base_dir, '.env'))


class Config:
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

    DEV_DATABASE_URL = "mysql+pymysql://${DEV_ADMIN_USER}:${DEV_ADMIN_PASS}@${DEV_URL}"
    DEV_DATABASE_ARGS = "{'ssl':{'ca':${CACERT}, 'check_hostname':False}}"
    DEV_DATABASE_URL_READ = "mysql+pymysql://${DEV_READ_USER}:${DEV_READ_PASS}@${DEV_URL}"
    DEV_DATABASE_URL_WRITE = "mysql+pymysql://${DEV_WRITE_USER}:${DEV_WRITE_PASS}@${DEV_URL}"
    DEV_DATABASE_URL_ADMIN = "mysql+pymysql://${DEV_ADMIN_USER}:${DEV_ADMIN_PASS}@${DEV_URL}"

    TEST_DATABASE_URL = "mysql+pymysql://${TEST_ADMIN_USER}:${TEST_ADMIN_PASS}@${TEST_URL}"
    TEST_DATABASE_ARGS = "{'ssl':{'ca':${CACERT}, 'check_hostname':False}}"
    TEST_DATABASE_URL_READ = "mysql+pymysql://${TEST_READ_USER}:${TEST_READ_PASS}@${TEST_URL}"
    TEST_DATABASE_URL_WRITE = "mysql+pymysql://${TEST_WRITE_USER}:${TEST_WRITE_PASS}@${TEST_URL}"
    TEST_DATABASE_URL_ADMIN = "mysql+pymysql://${TEST_ADMIN_USER}:${TEST_ADMIN_PASS}@${TEST_URL}"

    # export PROD environment vars
    PROD_DATABASE_URL = "mysql+pymysql://${PROD_ADMIN_USER}:${PROD_ADMIN_PASS}@${PROD_URL}"
    PROD_DATABASE_ARGS = "{'ssl':{'ca':${CACERT}, 'check_hostname':False}}"
    PROD_DATABASE_URL_READ = "mysql+pymysql://${PROD_READ_USER}:${PROD_READ_PASS}@${PROD_URL}"
    PROD_DATABASE_URL_WRITE = "mysql+pymysql://${PROD_WRITE_USER}:${PROD_WRITE_PASS}@${PROD_URL}"
    PROD_DATABASE_URL_ADMIN = "mysql+pymysql://${PROD_ADMIN_USER}:${PROD_ADMIN_PASS}@${PROD_URL}"
