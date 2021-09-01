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

## Function to flatten nested JSON
def flatten_json(nested_json, exclude=['']):
    """Flatten json object with nested keys into a single level.
        Args:
            nested_json: A nested json object.
            exclude: Keys to exclude from output.
        Returns:
            The flattened json object if successful, None otherwise.
    """
    out = {}

    def flatten(x, name='', exclude=exclude):
        if type(x) is dict:
            for a in x:
                if a not in exclude: flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out
#----------------------------- Loading data ----------------------------
def data_load():
    # Loading data from json file
    df = pd.read_json("./database.json")
    df = df.T
    return df

if __name__ == '__main__':
#----------------------- Inserting into SQLite database -------------------
    df = data_load()
        
    # Data cleaning
    df = df.reset_index().drop('index', axis=1)
    df['required_age'] = df['required_age'].apply(lambda x: str(x))
    df['developers'] = df['developers'].apply(list_str)
    df['genres'] = df['genres'].apply(get_all_desc, key_name=('description'))
    df['categories'] = df['categories'].apply(get_all_desc, key_name=('description'))


    df_price = pd.DataFrame([flatten_json(x) for x in df['price_overview']])

    df_platforms = pd.DataFrame([flatten_json(x) for x in df['platforms']])

    df_pc = pd.DataFrame([flatten_json(x) for x in df['pc_requirements']])

    df_mac = pd.DataFrame([flatten_json(x) for x in df['mac_requirements']])

    df_linux = pd.DataFrame([flatten_json(x) for x in df['linux_requirements']])

    df_releasedate = pd.DataFrame([flatten_json(x) for x in df['release_date']])

    #### Editing the columns

    ## Price
    df_price = df_price[['currency','final']]
    df_price['final']=df_price['final']/100
    df_price = df_price.rename(columns={'final':'price'})

    ## Windows/Linux/Mac Platform
    df_pc['minimum'] =  df_pc['minimum'].str.replace(r"<[^>]*>","")

    df_pc['recommended'] =  df_pc['recommended'].str.replace(r"<[^>]*>","")

    df_pc = df_pc.rename(columns={"minimum": "pc_minimum", "recommended": "pc_recommended"})

    df_mac['minimum'] =  df_mac['minimum'].str.replace(r"<[^>]*>","")

    df_mac['recommended'] =  df_mac['recommended'].str.replace(r"<[^>]*>","")

    df_mac = df_mac.rename(columns={"minimum": "mac_minimum", "recommended": "mac_recommended"})

    df_linux['minimum'] =  df_linux['minimum'].str.replace(r"<[^>]*>","")

    df_linux['recommended'] =  df_linux['recommended'].str.replace(r"<[^>]*>","")

    df_linux = df_linux.rename(columns={"minimum": "linux_minimum", "recommended": "linux_recommended"})

    ## Release Date

    df_releasedate["dates"] = pd.to_datetime(df_releasedate["date"], format='%d %b, %Y',errors='coerce')
    mask = df_releasedate.dates.isnull()
    print(df_releasedate.dates.isnull().sum())
    df_releasedate.loc[mask,'dates'] = pd.to_datetime(df_releasedate[mask]['date'],format='%b %Y',errors='coerce')
    mask = df_releasedate.dates.isnull()
    print(df_releasedate.dates.isnull().sum())
    df_releasedate.loc[mask,'dates'] = pd.to_datetime(df_releasedate[mask]['date'],format='%b %d, %Y',errors='coerce')
    df_releasedate = df_releasedate.drop(["date","coming_soon"], axis=1)

    ## Concact DF's
    df1 = df[['name','required_age','developers','website','is_free','num_reviews','review_score','header_image','short_description', 'genres', 'categories']]
    frames = [df1,df_price,df_platforms,df_pc,df_mac,df_linux,df_releasedate]

    df = pd.concat(frames, axis=1)


    # Selecting most important columns
    main_table = df[['name', 'required_age', 'developers', 'website', 'is_free',
       'num_reviews', 'review_score', 'genres', 'categories', 'header_image', 'windows', 'mac', 'linux', 'short_description']]
    
    price_table =df[['currency', 'price']]

    requirement_table = df[['pc_minimum', 'pc_recommended',
       'mac_minimum', 'mac_recommended', 'linux_minimum', 'linux_recommended']]


    for n in range(len(main_table)):
        name, required_age, developers, website, is_free, num_reviews, review_score,genres, categories, link, windows, mac,linux, short_description = main_table.iloc[n].values
        new_steam_game = SteamGame(name, required_age, developers, website, is_free, num_reviews, 
        review_score, genres, categories, link, windows, mac,linux, short_description)
        db.session.add(new_steam_game)

    for n in range(len(price_table)):
        currency, price = price_table.iloc[n].values
        new_steam_game = Price(currency, price)
        db.session.add(new_steam_game)

    for n in range(len(requirement_table)):
        pc_minimum, pc_recommended, mac_minimum, mac_recommended, linux_minimum, linux_recommended = requirement_table.iloc[n].values
        new_price_table = Requirement(pc_minimum, pc_recommended, mac_minimum,
        mac_recommended, linux_minimum, linux_recommended,)
        db.session.add(new_steam_game)

    db.session.commit()
    # df.to_sql(name='steam_game', con=db.engine, if_exists="append", index=False)
    print("database rows: ", len(SteamGame.query.all()))
    print("done")
#--------------------------------------------------------------------------