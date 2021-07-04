import pandas as pd
from pathlib import Path
from pandas.io.json import json_normalize
import datetime

def convert_date(date):
    return datetime.datetime.fromtimestamp(date).strftime('%d-%m-%Y')

df = pd.read_json(Path('data/test.json'), lines=True)
df = pd.json_normalize(df['data'])
# category.id 34 to gry planszowe
df = df[df['category.id'] == 34]

df = df[[
    'name',
    'goal', 
    'pledged', 
    'currency', 
    'currency_symbol', 
    'state',
    'country_displayable_name', 
    'backers_count', 
    'created_at',
    'launched_at',
    'deadline',
    'urls.web.project'
    ]]

df['created_at'] = pd.to_datetime(df['created_at'], unit='s')
df['launched_at'] = pd.to_datetime(df['launched_at'], unit='s')
df['deadline'] = pd.to_datetime(df['deadline'], unit='s')

df.to_csv("test.csv", index=False)