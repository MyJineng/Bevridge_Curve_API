import requests
import pandas as pd
import json
from pymongo import MongoClient
# Import your FRED API Key
from FRED_key import key

# Series Identifiers from FRED
ids = ['UNRATE', 'JTSJOR']

# Retrives all series and merges on basis of first series
for x in ids:
  request = f"https://api.stlouisfed.org/fred/series/observations?series_id={x}&api_key={key}&file_type=json"
  response = requests.get(request)
  series = pd.DataFrame(response.json()["observations"])
  series["value"] = series.rename(columns={'value': x}, inplace=True)
  series = series[['date', x]]
  if x == ids[0]:
    df = series
  else:
    df = pd.merge(df, series, on='date', how='inner')

# Select how to save dataframe
select = input("How would you like to save the data? csv or json: ")
if select == 'csv':
    df.to_csv('beveridge.csv', encoding='utf-8', index=False)
    print('Data Saved! Check local folder.')
elif select == 'json':
    df.to_json('beverdige.json', orient='records', lines=True)
    data = df.to_dict(orient='records')
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)
    mongo = MongoClient(port=27017)
    db = mongo["FRED_1"]
    collection = db["beveridge_curve"]
    for document in data:
        collection.insert_one(document)
    print('Data Saved!')
else:
    print("Data type not acceptable!")