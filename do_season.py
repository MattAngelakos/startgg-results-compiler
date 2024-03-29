from ql import *
from qlny import *
import pandas as pd
import json
from graphqlclient import GraphQLClient
import time
from do_stats import *
from do_statsny import *
from do_h2h import *
authToken = input('put in your key: ')
apiVersion = 'alpha'
client = GraphQLClient('https://api.start.gg/gql/' + apiVersion)
client.inject_token('Bearer ' + authToken)
val = input("What Region: ") 
if val == "NJ":
    players = pd.read_csv('players.csv')
    filename = 'players.csv'
elif val == "NY":
    players = pd.read_csv('players.csv')
    filename = 'players.csv'
else:
    raise ValueError
query = input("Do you want to preform the query? (Y or N): ")
stats = input("Do you want to preform the stats? (Y or N): ")
h2h = input("Do you want to preform the h2h? (Y or N): ")
if val == "NY":
    remove = input("Do you want to remove the losses? (Y or N): ")
if query.lower() == 'y':
    month_start, year_start = input("Enter month start and season year in the format ex: 10 2023 for 10/2023-12/2023: ").split()
    year_start=int(year_start)
    month_start=int(month_start)
    month_end = (month_start+3)
    if month_end > 12:
        year_end = year_start+1
    else:
        year_end = year_start
    month_end = month_end%12
    for i, row in players.iterrows():
        if row['playerId'] == 0:
            results = client.execute( 
            '''query EventQuery($slug: String) {
                user(slug: $slug) {
                    id
                    player {
                        id
                    }
                }
            },
            {
                "slug": '''+row['startggId']+'''
            }''')
            data = json.loads(results)
            print(data['data']['user']['player']['id'])
            row['playerId'] = data['data']['user']['player']['id']
            players.at[i, 'playerId'] = row['playerId']
            players.to_csv(filename, index=False)
        if val == "NJ":
            do_query(id=str(row['playerId']), year_start=year_start, month_start=month_start, day_start=1, hour_start=6, minute_start=0, year_end=year_end, month_end=month_end, day_end=1, hour_end=6, minute_end=0)
            pass
        elif val == "NY":
            ids = row['playerId']
            ids = str(ids)
            print(ids)
            do_querynewyork(id=ids, year_start=year_start, month_start=month_start, day_start=1, hour_start=6, minute_start=0, year_end=year_end, month_end=month_end, day_end=1, hour_end=6, minute_end=0)
            pass
        time.sleep(5)
if val == "NJ":
    if stats.lower() == 'y':
        do_the_stats('playersNJ.json', 'oorNJ.csv')
    if h2h.lower() == 'y':
        do_the_h2h('playersNJ.json','h2h.csv')
elif val == "NY":
    if stats.lower() == 'y':
        do_the_stats_ny('players.json', 'oorNY.csv')
    if h2h.lower() == 'y':
        do_the_h2h('players.json','h2hny.csv')
    if remove.lower() == 'y':
        killLosses()
kill = input("Do you want to remove any players?(Y or N): ")
if kill.lower() == 'y':
    while True:
        target = input("Enter player(enter to quit): ")
        if target == "":
            break
        if val == 'NJ':
            f = open('playersNJ.json')
        elif val == 'NY':
            f = open('players.json')
        data = json.load(f)
        data.pop(target, None)
        if val == 'NJ':
            data = saveJson(data, 'playersNJ.json')
        elif val == 'NY':
            data = saveJson(data, 'players.json')
"""bad_tourneys = pd.read_csv('bad_tournaments.csv')
name = "Highland Masters 59"
if not any(value in name for value in bad_tourneys['name'].astype(str)):
    print("hi")"""
#do_query(id=str(1216463), year_start=2023, month_start=10, day_start=1, hour_start=6, minute_start=0, year_end=2024, month_end=1, day_end=1, hour_end=6, minute_end=0)i