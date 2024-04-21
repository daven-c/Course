from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)  # Initialize flask app
CORS(app)  # Disable cross origin error

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydb.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)  # Creates database instance
