import os
import random
import string
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# ---pseudo random string used as secret key and anti forgery state token------
state = ''.join(random.choice(string.ascii_uppercase + string.digits) for
                x in range(32))
# --------------------------setup flask app------------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = state

# --------------------------setup database------------------------------------
# Creating the full file path regardless of your OS (linux, windows or mac)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
app.config['SQLALCHEMY_DATABASE_URI'] += os.path.join(basedir, 'data.db')
# This will avoid some warnings to be printed out
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

class SteamGame(db.Model):
    """This class represents a table steam_game in the database
    """
    __tablename__ = 'steam_game'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    is_free = db.Column(db.Boolean, nullable=False)
    num_reviews = db.Column(db.Integer, nullable=False)
    review_score = db.Column(db.Integer, nullable=False)

    def __init__(self, name, is_free, num_reviews, review_score) -> None:
        self.name = name
        self.is_free = is_free
        self.num_reviews = num_reviews
        self.review_score = review_score

    def __repr__(self):
        """This method helps to easily print an instance of the class"""
        return f"{self.name}"