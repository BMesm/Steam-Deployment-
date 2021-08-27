import os, json
import plotly
import plotly.express as px
import pandas as pd
from model import db, app, SteamGame
from flask import render_template

#----------------------------- Loading data ----------------------------
with open("database.json","r") as jsonFile:
    data = json.load(jsonFile)
df = pd.DataFrame(data)
df = df.T
df = df.reset_index().drop('index', axis=1)
df = df[['name','is_free','num_reviews','review_score']]

for n in range(len(df)):
    name, is_free, num_reviews, review_score = df.iloc[n].values
    new_steam_game = SteamGame(name, is_free, num_reviews, review_score)
    db.session.add(new_steam_game)
db.session.commit()
# df.to_sql(name='steam_game', con=db.engine, if_exists="append", index=False)
#--------------------------------------------------------------------------

@app.route('/')
def steam_game():

    fig = px.bar(df, x="num_reviews", y="review_score", color="is_free", barmode="group")  #, color="is_free",    barmode="group")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('index.html', graphJSON=graphJSON)

if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(debug=True, host='0.0.0.0', port=port)