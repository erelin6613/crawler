import os
import feedparser
import pandas as pd

for each in os.listdir('avvo_profiles'):
    df = pd.DataFrame()
    if str(os.path.join('avvo_profiles', each)).endswith('.csv'):
        continue
    with open(os.path.join('avvo_profiles', each), 'r') as file:
        f = file.read()
    for link in f.split('<loc>'):
        url = link.split('</loc>')[0]
        if '<?' in url:
            continue
        df = df.append({'url': link.split('</loc>')[0]}, ignore_index=True)
        print(df)
    filename = str(os.path.join('avvo_profiles', each))[:-4]+'.csv'
    df.to_csv(each.split('.')[0]+'.csv')
    break

