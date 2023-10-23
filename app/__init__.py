from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from dotenv import load_dotenv
from app.utils import mail
import os

app = Flask(__name__)

load_dotenv()

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')

# File upload path
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER')

# Mail server configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS')
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

# app.secret_key = "supersecretkey"  # for flashing messages
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Initialise mail object
mail.init_app(app)

# Enable CORS for all routes
CORS(app)

from app import views

