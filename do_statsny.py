import json
import re
import pandas as pd
from graphqlclient import GraphQLClient
from do_stats import *
authToken = '838bca69b8fcc334b7606c19a4b6449a'
apiVersion = 'alpha'
client = GraphQLClient('https://api.start.gg/gql/' + apiVersion)
client.inject_token('Bearer ' + authToken)
def do_the_stats_ny(playerJson, oorcsv):
    f = open(playerJson)
    data = json.load(f)
    df = pd.read_csv(oorcsv)
    dfLumi = pd.read_csv('lumirank.csv')
    for player, playerData in data.items():
        #if(playerData['eligible']):
            for wins in playerData['wins']:
                print(wins)
                noteable = df[df['tag'] == wins['tag']]
                if not noteable.empty:
                    winData = noteable.iloc[0].to_dict()
                    winData['numOfWins'] = wins['numOfWins']
                    if winData not in playerData['noteableWins']:
                        playerData['noteableWins'].append(winData)
                lumirank = dfLumi[dfLumi['tag'] == wins['tag']]
                if not lumirank.empty:
                    winData = lumirank.iloc[0].to_dict()
                    capOrFact = do_verification(winData['id'], wins['winnerId'])
                    if capOrFact:
                        winData['numOfWins'] = wins['numOfWins']
                        if winData not in playerData['noteableWins']:
                            playerData['noteableWins'].append(winData)
    with open(playerJson, 'w') as file:
          json.dump(data, file, indent=2)