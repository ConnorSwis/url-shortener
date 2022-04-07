from flask import Flask
from config import Config
import os


app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'src', 'templates'))
app.config.from_object(Config)
app.static_folder = os.path.join(os.getcwd(), 'src', 'static')

from app import routes