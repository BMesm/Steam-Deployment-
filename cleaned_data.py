import json
import pandas as pd
from model import SteamGame, db

def get_all_desc(x,key_name):
    try:
        str_list = ''
        for i in x:
            desc = i.get(key_name)
            str_list += desc
            str_list += ', '
        return str_list[:-2]
    except (TypeError):
        pass

def list_str(x):
    try:
        return ', '.join([str(item) for item in x])
    except (TypeError):
        pass

#----------------------------- Loading data ----------------------------
def data_load():
    df_original = pd.read_json("./database.json")
    df = df.T
    df = df.reset_index().drop('index', axis=1)
    df = df[['name', 'required_age', 'is_free','review_score'
       'short_description', 'header_image', 'website', 'developers',
       'platforms', 'categories', 'genres', 'screenshots', 'movies',
       'controller_support', 'dlc', 'reviews']]
    return df



if __name__ == '__main__':
    
    df = data_load()
#------------------------------- Cleaning data ----------------------------

df.developers = df.developers.apply(list_str)

df['work_on_windows'] = df['platforms'].apply(lambda x: x.get('windows'))
df['work_on_mac'] = df['platforms'].apply(lambda x: x.get('mac'))
df['work_on_linux'] = df['platforms'].apply(lambda x: x.get('linux'))
df = df.drop('platforms',axis=1)

df['genre'] = df['genres'].apply(get_all_desc, key_name=('description'))
df['categories'] = df['categories'].apply(get_all_desc, key_name=('description'))



#----------------------- Inserting into SQLite database -------------------
    for n in range(len(df)):
        name, is_free, num_reviews, review_score = df.iloc[n].values
        new_steam_game = SteamGame(name, is_free, num_reviews, review_score,
        short_description, header_image, website, developers, platforms, categories,
        genres, screenshots, movies, controller_support, dlc, reviews)
        db.session.add(new_steam_game)
    db.session.commit()
    # df.to_sql(name='steam_game', con=db.engine, if_exists="append", index=False)
    print("done")
#--------------------------------------------------------------------------