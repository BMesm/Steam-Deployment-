import os
import random
from re import S
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
    header_image = db.Column(db.String(400))
    price = db.Column(db.Float)
    genres = db.Column(db.String(400))
    categories = db.Column(db.String(400))
    developers = db.Column(db.String(400))
    short_description = db.Column(db.Text)
    website = db.Column(db.String(400))
    windows = db.Column(db.Boolean)
    mac = db.Column(db.Boolean)
    linux = db.Column(db.Boolean)

    # This connect SteamGame to Price
    # So we can access price from SteamGame
    prices = db.relationship('Price', lazy=True)
    # requirements = db.relationship('Requirement', lazy=True)

    def __init__(self, name, required_age,  is_free, num_reviews, review_score, header_image,price, 
                genres, categories, developers, short_description, website, windows, mac,linux) -> None:
        self.name = name
        self.required_age = required_age
        self.is_free = is_free
        self.num_reviews = num_reviews
        self.review_score = review_score
        self.header_image = header_image
        self.price = price
        self.genres = genres
        self.categories = categories
        self.developers = developers
        self.short_description = short_description
        self.website = website
        self.windows = windows
        self.mac = mac
        self.linux = linux

    def __repr__(self):
        """This method helps to easily print an instance of the class"""
        return f"{self.name} - {self.price}"


class Price(db.Model):
    """This class represents a table prices in the database
    """
    __tablename__ = 'prices'

    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(10))
    price = db.Column(db.Float)
    # Connecting Price to SteamGame with a Foreign Key
    game_id = db.Column(db.Integer, db.ForeignKey('steam_game.id'))

    def __init__(self, currency, price) -> None:
        self.currency = currency
        self.price = price


# class Requirement(db.Model):
#     """This class represents a table requirement in the database
#     """
#     __tablename__ = 'requirement'

#     id = db.Column(db.Integer, primary_key=True)
#     pc_minimum = db.Column(db.String(400))
#     pc_recommended = db.Column(db.String(400))
#     mac_minimum = db.Column(db.String(400))
#     mac_recommended = db.Column(db.String(400))
#     linux_minimum = db.Column(db.String(400))
#     linux_recommended = db.Column(db.String(400))
#     # Connecting Requirement to SteamGame with a ForeignKey
#     game_id = db.Column(db.Integer, db.ForeignKey('steam_game.id'))

#     def __init__(self, pc_minimum, pc_recommended, mac_minimum,
#                 mac_recommended, linux_minimum, linux_recommended) -> None:
#         self.pc_minimum = pc_minimum
#         self.pc_recommended = pc_recommended
#         self.mac_minimum = mac_minimum
#         self.mac_recommended = mac_recommended
#         self.linux_minimum = linux_minimum
#         self.linux_recommended = linux_recommended