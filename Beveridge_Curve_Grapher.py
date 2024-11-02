import pandas as pd
import json
import seaborn as sns
import matplotlib.pyplot as plt
from pymongo import MongoClient

def beveridge_curve_graph(dataframe):
    print(df)
    bins = [
    '2000-12-01',  # Dec 2000
    '2001-02-28',  # Feb 2001
    '2001-11-30',  # Nov 2001
    '2007-11-30',  # Nov 2007
    '2009-06-30',  # June 2009
    '2020-02-29',  # Feb 2020
    '2020-04-30',  # Apr 2020
    '2024-09-30',  # Sep 2024
    ]

    # Define labels for each bucket
    labels = [
    'Dec 2000 - Feb 2001',
    'Mar 2001 - Nov 2001',
    'Dec 2001 - Nov 2007',
    'Dec 2007 - Jun 2009',
    'Jul 2009 - Feb 2020',
    'Mar 2020 - Apr 2020',
    'May 2020 - Sep 2024',
    ]
    bins = pd.to_datetime(bins)
    df['date_bucket'] = pd.cut(df['date'], bins=bins, labels=labels, right=True, include_lowest=True)

    # Creates a color palette based on the number of economic cycles
    unique_buckets = df['date_bucket'].unique()
    palette = sns.color_palette("viridis", len(unique_buckets))
    # Create graph
    plt.figure(figsize=(10, 6))
    # Loop through each cycle and plot
    for i, bucket in enumerate(unique_buckets):
        bucket_data = df[df['date_bucket'] == bucket]
        # Scatter plot for the cycle
        sns.scatterplot(data=bucket_data, x='UNRATE', y='JTSJOR', label=bucket, color=palette[i])
        # Sorts the data by date for the line plot
        bucket_data_sorted = bucket_data.sort_values('date')
        # Line plot connecting the points in the current cycle
        plt.plot(bucket_data_sorted['UNRATE'], bucket_data_sorted['JTSJOR'], marker='o', linestyle='-', color=palette[i])
    # Line to display Full Employment Scenario
    max_value = max(df['UNRATE'].max(), df['JTSJOR'].max())
    plt.plot([2, max_value], [2, max_value], color='red', linestyle='--', linewidth=2, label='Ideal Labor Market')
    plt.xlim(left=3)
    plt.ylim(bottom=1, top=8)

    plt.title('Beveridge Curve: Unemployment Rate vs. Job Vacancy Rate')
    plt.xlabel('Unemployment Rate (%)')
    plt.ylabel('Job Vacancy Rate (%)')
    plt.grid()
    plt.legend(title='Economic Cycles', bbox_to_anchor=(0.8, 1), loc='upper left')
    plt.show()
    plt.tight_layout()

# Select how to load dataframe data
select = input('How would you like to load the data? csv or json: ')
if select == 'csv':
    df = pd.read_csv(r'beveridge.csv')
    df['date'] = pd.to_datetime(df['date'])
    beveridge_curve_graph(df)
elif select == 'json':
    mongo = MongoClient(port=27017)
    db = mongo["FRED"]
    collection = db["beveridge_curve"]
    data = (collection.find())
    dat = []

    for document in data:
        document['_id'] = str(document['_id'])
        dat.append(document)

    json_data = json.dumps(dat)
    df = pd.read_json(json_data, orient='records')
    df = df.drop(columns='_id')
    beveridge_curve_graph(df)
else:
    print("Data type not acceptable!")