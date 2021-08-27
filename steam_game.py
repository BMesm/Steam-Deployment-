import os
import json
import plotly
import plotly.express as px
from model import app
from loading_data import data_load
from flask import render_template

# loading data
df = data_load()

@app.route('/')
def steam_game():

    fig = px.bar(df, x="num_reviews", y="review_score", color="is_free", barmode="group")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('index.html', graphJSON=graphJSON)

if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(debug=True, host='0.0.0.0', port=port)