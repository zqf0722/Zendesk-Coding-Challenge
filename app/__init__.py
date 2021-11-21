from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from flask_moment import Moment

# Init the application
app = Flask(__name__)
# Load the configuration from config.py
app.config.from_object(Config)
# Load flask_bootstrap
bootstrap = Bootstrap(app)
# Load flask_moment
moment = Moment(app)

# Import routes and error
from app import routes, error
