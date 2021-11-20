import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    # Authorization
    EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
    API_TOKEN = os.environ.get('API_TOKEN')
    SUB_DOMAIN = os.environ.get('SUB_DOMAIN')
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'serene-joker'
