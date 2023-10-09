from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/rpl_murdoch'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "supersecretkey"  # for flashing messages
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Enable CORS for all routes
CORS(app)

from app import views

