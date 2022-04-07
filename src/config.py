import os

from dotenv import load_dotenv
load_dotenv('../.env')

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'ooga booga')
    DEBUG = bool(os.getenv('DEBUG', True))