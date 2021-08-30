import os
import json
import plotly
import plotly.express as px
from model import *
from loading_data import data_load
from flask import render_template, request

# loading data
df = data_load()

@app.route('/vizualisation')
def vizualisation():
    fig = px.bar(df, x="num_reviews", y="review_score", color="is_free", barmode="group")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('vizualisation.html', graphJSON=graphJSON)
    
 

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['search_string']
        search = "%{}%".format(query)
        searchresults = SteamGame.query.filter(SteamGame.name.like(search)).all()
        return render_template('search.html', searchtable = searchresults)
    else:
        return render_template('index.html')

@app.route("/view")
def view():
    return render_template("view.html", values = SteamGame.query.all())

if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(debug=True, host='0.0.0.0', port=port)
