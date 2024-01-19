from ql import *
from qlny import *
import pandas as pd
import json
from graphqlclient import GraphQLClient
import time
from do_stats import *
from do_statsny import *
from do_h2h import *
authToken = '838bca69b8fcc334b7606c19a4b6449a'
apiVersion = 'alpha'
client = GraphQLClient('https://api.start.gg/gql/' + apiVersion)
client.inject_token('Bearer ' + authToken)
val = input("What Region: ") 
if val == "NJ":
    players = pd.read_csv('playersTest.csv')
    filename = 'playersTest.csv'
elif val == "NY":
    players = pd.read_csv('playersTest.csv')
    filename = 'playersTest.csv'
else:
    raise ValueError
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
            "slug": ""+row['startggId']+""
        }''')
        data = json.loads(results)
        print(data['data']['user']['player']['id'])
        row['playerId'] = data['data']['user']['player']['id']
        players.at[i, 'playerId'] = row['playerId']
        players.to_csv(filename, index=False)
    if val == "NJ":
        do_query(id=str(row['playerId']), year_start=2023, month_start=10, day_start=1, hour_start=6, minute_start=0, year_end=2024, month_end=1, day_end=1, hour_end=6, minute_end=0)
    elif val == "NY":
        do_querynewyork(id=str(row['playerId']), year_start=2023, month_start=10, day_start=1, hour_start=6, minute_start=0, year_end=2024, month_end=1, day_end=1, hour_end=6, minute_end=0)
    time.sleep(5)
if val == "NJ":
    do_the_stats('playersTest.json', 'oor.csv')
    do_the_h2h('playersTest.json','h2h.csv')
elif val == "NY":
    do_the_stats_ny('players.json', 'oor.csv')
    do_the_h2h('players.json','h2hny.csv')
    killLosses()
#do_query(id=str(1216463), year_start=2023, month_start=10, day_start=1, hour_start=6, minute_start=0, year_end=2024, month_end=1, day_end=1, hour_end=6, minute_end=0)