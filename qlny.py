from graphqlclient import GraphQLClient
import json
import pandas as pd
import re
import datetime
import time
from ql import *
authToken = '838bca69b8fcc334b7606c19a4b6449a'
apiVersion = 'alpha'
client = GraphQLClient('https://api.start.gg/gql/' + apiVersion)
client.inject_token('Bearer ' + authToken)
def do_querynewyork(id, year_start, month_start, day_start, hour_start, minute_start, year_end, month_end, day_end, hour_end, minute_end):
    date_time_start = datetime.datetime(year_start, month_start, day_start, hour_start, minute_start)
    date_time_unix_start = int((time.mktime(date_time_start.timetuple())))
    date_time_unix_start = str(date_time_unix_start)
    date_time_end = datetime.datetime(year_end, month_end, day_end, hour_end, minute_end)
    date_time_unix_end = int((time.mktime(date_time_end.timetuple())))
    date_time_unix_end = str(date_time_unix_end)
    results = client.execute('''
    query Standings {
        player(id: '''+id+''') {
        gamerTag
        recentStandings(videogameId: 1386, limit: 20){
            placement
                entrant{
                name
            }
            container {
            ... on Event{
            id
            name
            tournament{
              name
              addrState
            }
            startAt
            isOnline
            numEntrants
          }
        }
      }
    }
    }''')
    data = json.loads(results)
    try:
        f2 = open('players.json')
        dataPlayers = json.load(f2)
    except:
        dataPlayers = {}
    tag = data['data']['player']['gamerTag']
    eligible = False
    if tag not in dataPlayers:
        new_player_data = {
            "PlayerName": tag,
            "altTags": [],
            "eligible": eligible,
            "wins": [],
            "noteableWins": [],
            "losses": []
        }
        dataPlayers[tag] = new_player_data
        dataPlayers = saveJson(dataPlayers, 'players.json')
    tourneys = pd.read_csv('tournaments.csv')
    bad_tourneys = pd.read_csv('bad_tournaments.csv')   
    def add_row_to_tourneys(csv_file, new_row):
      df = pd.read_csv(csv_file)
      df = df._append(pd.Series(new_row, index=df.columns), ignore_index=True)
      df.to_csv(csv_file, index=False)
    print('Current results acquired...')
    threeNYBrackets = False
    numNYBrackets = 0
    for key, value in enumerate(data['data']['player']['recentStandings']):
        if not threeNYBrackets:
            if numNYBrackets == 4:
                threeNYBrackets = True
        name = value['container']['tournament']['name']
        entrant_count = value['container']['numEntrants']
        eventName = str(value['container']['name']).lower()
        if name not in tourneys['tournament_name'].values:
            if not any(value in name for value in bad_tourneys['name'].astype(str)):
                entrant_count = value['container']['numEntrants']
                if if1(date_time_unix_start, date_time_unix_end, value, entrant_count, 'standings'): 
                    if if2(eventName):
                        tourneys = do_tiering(add_row_to_tourneys, name, entrant_count, name)
                else:
                    bad_tourneys = addAndGetRow(add_row_to_tourneys, [name], 'bad_tournaments.csv')
            else:
                foundBracket = tourneys[tourneys['tournament_name'] == name]
            if value['container']['tournament']['addrState'] == "NY":
                numNYBrackets+=1
            entrantTag = value['entrant']['name']
            if(entrantTag != tag and if2(eventName)):
                if(entrantTag not in dataPlayers[tag]['altTags']):
                    print(1)
                    dataPlayers[tag]['altTags'].append(entrantTag)
    if(threeNYBrackets):
        dataPlayers[tag]['eligible'] = True
    with open('players.json', 'w') as file:
        json.dump(dataPlayers, file, indent=2)
    f2 = open('players.json')
    dataPlayers = json.load(f2)
    time.sleep(1)
    results = client.execute(
    '''query Sets{
	player(id: '''+id+''') {
    sets(perPage: 150, page: 1, filters:{updatedAfter:'''+date_time_unix_start+'''}) {
        nodes {
          displayScore
          winnerId
          event {
            id
            name
            videogame {
              id
            }
            tournament {
              name
            }
            startAt
            isOnline
            numEntrants
          }
        }
      }
    }
    }''')
    data = json.loads(results)
    for key, value, in enumerate(data['data']['player']['sets']['nodes']):
        nameT = value['event']['tournament']['name']
        if nameT in tourneys['tournament_name'].values:
            dataPlayers = doRecordNew(dataPlayers, tag, tourneys, value, nameT, id)
        else:
            if not any(value in nameT for value in bad_tourneys['name'].astype(str)):
                entrant_count = value['event']['numEntrants']
                eventName = value['event']['name']
                if if1(date_time_unix_start, date_time_unix_end, value, entrant_count, 'sets'): 
                    if if2(eventName):
                        tourneys = do_tiering(add_row_to_tourneys, name, entrant_count, nameT)
                        dataPlayers = doRecordNew(dataPlayers, tag, tourneys, value, nameT, id)
                else:
                    bad_tourneys = addAndGetRow(add_row_to_tourneys, [nameT], 'bad_tournaments.csv')
    dataPlayers = saveJson(dataPlayers, 'players.json')
    dataPlayers[tag]['losses'] = sorted(dataPlayers[tag]['losses'], key=lambda x: (-x['numOfLosses'], x['tag'].lower()))
    dataPlayers[tag]['wins'] = sorted(dataPlayers[tag]['wins'], key=lambda x: (-x['numOfWins'], x['tag'].lower()))
    dataPlayers = saveJson(dataPlayers, 'players.json')
    return

def doRecordNew(dataPlayers, tag, tourneys, value, nameT, id):
    eventNameSet = value['event']['name']
    if(value['displayScore'] != 'DQ' and value['event']['videogame']['id'] == 1386
        and if2(eventNameSet)):
      parts = re.split(r'\s-\s', value['displayScore'])
      if len(parts) == 2:
        if parts[0][-1] == "W":
          score0 = 1
          score1 = 0
        elif parts[0][-1] == "L":
          score0 = 0
          score1 = 1
        else:
          score0 = int(parts[0][-1])
          score1 = int(parts[1][-1])
        tag0 = parts[0][:-2]
        tag1 = parts[1][:-2]
        tag0 = re.sub(r'^.*\|\s*', '', tag0)
        tag1 = re.sub(r'^.*\|\s*', '', tag1)
        if tag0 != tag and tag1 != tag and tag0 not in dataPlayers[tag]['altTags'] and tag1 not in dataPlayers[tag]['altTags']:
          new_tag = do_findAlt(value['event']['id'], id)
          dataPlayers[tag]['altTags'].append(new_tag)
        foundBracket = tourneys[tourneys['tournament_name'] == nameT]
        tier = int(foundBracket['tier'].iloc[0])
        if (score0 > score1 and (tag0 == tag or tag0 in dataPlayers[tag]['altTags'])) or (score0 < score1 and (tag0 != tag and tag0 not in dataPlayers[tag]['altTags'])):
          if tag0 == tag or tag0 in dataPlayers[tag]['altTags']:
            opTag = tag1
          else:
            opTag = tag0
          winnerId = value['winnerId']
          dataPlayers = addWinsNew(dataPlayers, tag, value, tier, nameT, opTag, winnerId)
        else:
          dataPlayers = addLossNew(dataPlayers, tag, value, tier, nameT, tag0, tag1)
    return dataPlayers

def addWinsNew(dataPlayers, tag, value, tier, nameT, opTag, winnerId):
    matching_entry = next((entry for entry in dataPlayers[tag]['wins'] if entry['tag'] == opTag), None)
    if matching_entry:
      matching_entry['numOfWins']+=1
      matching_entry['winnerId'].append(winnerId)
    else:
      new_win_info = {"tag": opTag, 'numOfWins': 1, "winnerId": [winnerId]}
      dataPlayers[tag]['wins'].append(new_win_info)
    return dataPlayers

def addLossNew(dataPlayers, tag, value, tier, nameT, tag0, tag1):
    if tag0 == tag or tag0 in dataPlayers[tag]['altTags']:
      opTag = tag1
    else:
      opTag = tag0
    matching_entry = next((entry for entry in dataPlayers[tag]['losses'] if entry['tag'] == opTag), None)
    if matching_entry:
      matching_entry['numOfLosses']+=1
    else:
      new_loss_info = {"tag": opTag, 'numOfLosses': 1}
      dataPlayers[tag]['losses'].append(new_loss_info)
    return dataPlayers

def killLosses():
    f = open('players.json')
    data = json.load(f)
    for player in data:
        data[player].pop('losses', None)
    data = saveJson(data, 'players.json')