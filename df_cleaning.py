import pandas as pd
import json

with open("database.json") as f:
    data = json.load(f)

df_copy = pd.DataFrame(data)

df = df_copy.T
df = df.reset_index()

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

### Creating the columns

df_genres = pd.DataFrame([flatten_json(x) for x in df['genres']])

df_price = pd.DataFrame([flatten_json(x) for x in df['price_overview']])

df_categories = pd.DataFrame([flatten_json(x) for x in df['categories']])

df_screenshots = pd.DataFrame([flatten_json(x) for x in df['screenshots']])

df_platforms = pd.DataFrame([flatten_json(x) for x in df['platforms']])

df_pc = pd.DataFrame([flatten_json(x) for x in df['pc_requirements']])

df_mac = pd.DataFrame([flatten_json(x) for x in df['mac_requirements']])

df_linux = pd.DataFrame([flatten_json(x) for x in df['linux_requirements']])

df_releasedate = pd.DataFrame([flatten_json(x) for x in df['release_date']])

#### Editing the columns

## Genres

df_genres = df_genres[['0_id', '0_description', '1_id', '1_description',]]
df_genres = df_genres.drop(columns = ["0_id","1_id"], axis = 1)
df_genres = df_genres.rename(columns={"0_description": "primary_genre", "1_description": "secondary_genre"})

## Price
df_price = df_price[['currency','final']]
df_price['final']=df_price['final']/100
df_price = df_price.rename(columns={'final':'price'})

## Categories
df_categories = df_categories[['0_id', '0_description', '1_id', '1_description', '2_id',
       '2_description', '3_id', '3_description', '4_id', '4_description']]

df_categories = df_categories.drop(columns =["0_id","1_id","2_id","2_description",
                                             "3_id","3_description","4_id","4_description"])

df_categories = df_categories.rename(columns={"0_description": "primary_category", "1_description": "secondary_category"})

## Screenshots
df_screenshots = df_screenshots[['0_path_full']]
df_screenshots = df_screenshots.rename(columns={"0_path_full": "screenshot"})

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
df1 = df[['name','required_age','developers','website','is_free','num_reviews','review_score']]
frames = [df1,df_genres,df_price,df_categories,df_screenshots,df_platforms,
        df_pc,df_mac,df_linux,df_releasedate]

df = pd.concat(frames, axis=1)


print(df.columns)
print(df.head())
print(df.info())

