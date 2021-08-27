import json
import pandas as pd
from model import SteamGame, db

#----------------------------- Loading data ----------------------------
def data_load():
    with open("database.json","r") as jsonFile:
        data = json.load(jsonFile)
    df = pd.DataFrame(data)
    df = df.T
    df = df.reset_index().drop('index', axis=1)
    df = df[['name','is_free','num_reviews','review_score']]
    return df

df = data_load()

if __name__ == '__main__':
#----------------------- Inserting into SQLite database -------------------
    for n in range(len(df)):
        name, is_free, num_reviews, review_score = df.iloc[n].values
        new_steam_game = SteamGame(name, is_free, num_reviews, review_score)
        db.session.add(new_steam_game)
    db.session.commit()
    # df.to_sql(name='steam_game', con=db.engine, if_exists="append", index=False)
    print("done")
#--------------------------------------------------------------------------