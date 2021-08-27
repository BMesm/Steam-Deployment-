import os, json
import plotly
import plotly.express as px
import pandas as pd
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)


# --------------------------setup database------------------------------------
# Creating the full file path regardless of your OS (linux, windows or mac)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
app.config['SQLALCHEMY_DATABASE_URI'] += os.path.join(basedir,'data.db')
# This will avoid some warnings to be printed out
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
#Migrate(app, db)

class SteamGame(db.Model):
    """This class represents a table steam_game in the database
    """
    __tablename__ = 'steam_game'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    is_free = db.Column(db.Boolean, nullable=False)
    num_reviews = db.Column(db.Integer, nullable=False)
    review_score = db.Column(db.Integer, nullable=False)
    

    def __repr__(self):
        """This method helps to easily print an instance of the class"""
        return f"{self.name}"

#----------------------------- Loading data ----------------------------
with open("database.json","r") as jsonFile:
    data = json.load(jsonFile)
df = pd.DataFrame(data)
df = df.T
df = df.reset_index().drop('index', axis=1)
df = df[['name','is_free','num_reviews','review_score']]

df.to_sql(name='steam_game', con=db.engine, if_exists="append", index=False)
#--------------------------------------------------------------------------

@app.route('/')
def steam_game():

    fig = px.bar(df, x="num_reviews", y="review_score", color="is_free", barmode="group")  #, color="is_free",    barmode="group")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('index.html', graphJSON=graphJSON)

if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(debug=True, host='0.0.0.0', port=port)