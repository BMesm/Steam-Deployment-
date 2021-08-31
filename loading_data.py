import json
import pandas as pd
from model import SteamGame, db

#------------------------------ SOME CLEANING FUNCTIONS ---------------------
#to get several description
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

# List to string
def list_str(x):
    try:
        return ', '.join([str(item) for item in x])
    except (TypeError):
        pass

# extracting price from price_overview
def get_price(x,key_name):
    try:
        output = x.get(key_name)
        return output[:-1].replace(',','.')
    except:
        pass
#----------------------------- Loading data ----------------------------
def data_load():
    # Loading data from json file
    df = pd.read_json("./database.json")
    df = df.T
    # Data cleaning
    df = df.reset_index().drop('index', axis=1)
    df['required_age'] = df['required_age'].apply(lambda x: str(x))
    df.developers = df.developers.apply(list_str)
    df['windows'] = df['platforms'].apply(lambda x: x.get('windows'))
    df['mac'] = df['platforms'].apply(lambda x: x.get('mac'))
    df['linux'] = df['platforms'].apply(lambda x: x.get('linux'))
    df = df.drop('platforms',axis=1)
    df['genres'] = df['genres'].apply(get_all_desc, key_name=('description'))
    df['categories'] = df['categories'].apply(get_all_desc, key_name=('description'))
    df['price'] = df['price_overview'].apply(get_price,key_name='final_formatted')

    # Selecting most important columns
    df = df[['name', 'required_age', 'is_free','num_reviews','review_score', 'price','genres',  
             'developers', 'short_description', 'header_image', 'website', 'windows', 
             'mac', 'linux', 'categories']]
    print("dataframe rows: ", df.shape)
    return df

if __name__ == '__main__':
#----------------------- Inserting into SQLite database -------------------
    df = data_load()

    for n in range(len(df)):
        name, required_age, is_free, num_reviews, review_score, price, genres,developers, short_description, header_image, website, windows,mac, linux, categories = df.iloc[n].values
        new_steam_game = SteamGame(name, required_age, is_free, num_reviews, review_score,price, genres, developers, short_description, header_image, website, windows,mac, linux, categories)
        db.session.add(new_steam_game)
    db.session.commit()

    # df.to_sql(name='steam_game', con=db.engine, if_exists="append", index=False)
    print("database rows: ", len(SteamGame.query.all()))
    print("done")
#--------------------------------------------------------------------------