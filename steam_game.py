import os
import json
import plotly
import plotly.express as px
from model import *
from loading_data import data_load
from flask import render_template, request

# loading data
df = data_load()

@app.route('/')
def steam_game():
    return render_template('index.html')

@app.route('/vizualisation')
def vizualisation():
    # Bar plot
    fig1 = px.bar(df, x="num_reviews", y="review_score", color="is_free", barmode="group")
    fig1.update_layout(title_text='Relationship between number of reviews and their score', title_x=0.5)
    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    # Scatter Plot
    fig2 = px.scatter(df, x="num_reviews", y="review_score", color="is_free")
    fig2.update_layout(title_text='Scatter Plot', title_x=0.5)
    graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    fig3 = px.histogram(df, x="is_free")
    fig3.update_layout(title_text='Amount of free and paid games', title_x=0.5)
    graph3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('vizualisation.html', graph1=graph1JSON, graph2=graph2JSON,
                                                graph3=graph3JSON)
    
 

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
    app.run(debug=True, port=port)