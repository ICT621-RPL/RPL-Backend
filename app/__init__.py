from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/rpl_murdoch'
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Enable CORS for all routes
CORS(app)

from app import views
