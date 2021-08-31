import os
import random
import string
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

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
    required_age = db.Column(db.Integer)
    is_free = db.Column(db.Boolean, nullable=False)
    num_reviews = db.Column(db.Integer, nullable=False)
    review_score = db.Column(db.Integer, nullable=False)
    price = db.Column(db.String(400))
    genres = db.Column(db.String(400))
    developers = db.Column(db.String(400))
    short_description = db.Column(db.Text)
    header_image = db.Column(db.String(400))
    website = db.Column(db.String(400))
    windows = db.Column(db.Boolean)
    mac = db.Column(db.Boolean)
    linux = db.Column(db.Boolean)
    categories = db.Column(db.String(400))

    def __init__(self, name, required_age, is_free, num_reviews, review_score, 
                 price, genres, developers, short_description, header_image, 
                 website, windows, mac, linux, categories) -> None:
        self.name = name
        self.required_age = required_age
        self.is_free = is_free
        self.num_reviews = num_reviews
        self.review_score = review_score
        self.price = price
        self.genres = genres
        self.developers = developers
        self.short_description = short_description
        self.header_image = header_image
        self.website = website
        self.windows = windows
        self.mac = mac
        self.linux = linux
        self.categories = categories

    def __repr__(self):
        """This method helps to easily print an instance of the class"""
        return f"{self.name} - {self.price}"