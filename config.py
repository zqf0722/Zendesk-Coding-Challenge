import os
from dotenv import load_dotenv

# Load environment arguments from .env file
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    # Authorization
    EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
    API_TOKEN = os.environ.get('API_TOKEN')
    SUB_DOMAIN = os.environ.get('SUB_DOMAIN')
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'serene-joker'
    # How many tickets are showing per page
    TICKETS_PER_PAGE = os.environ.get('TICKETS_PER_PAGE') or 25