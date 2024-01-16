import json
import re
import pandas as pd
from graphqlclient import GraphQLClient
f = open('playersTest.json')
data = json.load(f)
df = pd.read_csv('oor.csv')
dfLumi = pd.read_csv('lumirank.csv')
pattern = r'^(.*?)(?=\s\d|\s#)'
authToken = '838bca69b8fcc334b7606c19a4b6449a'
apiVersion = 'alpha'
client = GraphQLClient('https://api.start.gg/gql/' + apiVersion)
client.inject_token('Bearer ' + authToken)
def do_verification(player_id, winnerIds):
    verification = client.execute('''
    query Sets{
	    player(id: '''+str(player_id)+''') {
            sets(perPage: 200, page: 1, filters:{updatedAfter:1696154400}) {
                nodes {
                    winnerId
                    displayScore
                }
            }
        }
    }''')
    verificationData = json.loads(verification)
    try:
        nodes = verificationData['data']['player']['sets']['nodes']
        dfVerification = pd.DataFrame(nodes)
        for id in winnerIds:
            mask = dfVerification[dfVerification['winnerId'] == id]
            if mask.empty:
                return False
        return True
    except KeyError:
        print("error")
        return False
for player, playerData in data.items():
    if(playerData['eligible']):
        '''print(player)
        allWins = 0
        allLosses = 0
        playerBrackets = []
        numOfUniqueBrackets = 0
        for i in range(1, 6):
            avgPlacement = 0
            numOfBrackets = 0
            numOfWinsTotal = 0
            numOfLossesTotal = 0
            for tiertourney, tiertourneyData in playerData['Tier'+str(i)+'Brackets'].items():
                if(tiertourney != "avgPlacement" and tiertourney != "record" and tiertourney != "winrate"):
                    numOfWins = 0
                    numOfLosses = 0
                    if not (tiertourneyData['losses'] == [] and tiertourneyData['wins'] == []):
                        for wins in tiertourneyData['wins']:
                            numOfWins+=wins['numOfWins']
                        for losses in tiertourneyData['losses']:
                            numOfLosses+=losses['numOfLosses']
                        print(f"Tournery: {tiertourney}, Placement: {tiertourneyData['placement']}, Record: {numOfWins}-{numOfLosses}")
                        avgPlacement += tiertourneyData['placement']
                        numOfBrackets+=1
                        numOfWinsTotal+=numOfWins
                        numOfLossesTotal+=numOfLosses
                        tiertourneyData['record']=str(numOfWins)+"-"+str(numOfLosses)
                        if(i == 4 or i ==5):
                            numOfUniqueBrackets+=1
                        else:
                            unique = True
                            for s in playerBrackets:
                                if s in tiertourney.lower():
                                    unique = False
                            if unique:
                                match = re.match(pattern, tiertourney.lower())
                                if match:
                                    result = match.group(1)
                                    playerBrackets.append(result)                                        
                                numOfUniqueBrackets+=1
            if numOfBrackets:
                avgPlacement = avgPlacement/numOfBrackets
                playerData['Tier'+str(i)+'Brackets']['avgPlacement']=avgPlacement
                playerData['Tier'+str(i)+'Brackets']['record']=str(numOfWinsTotal)+"-"+str(numOfLossesTotal)
                playerData['Tier'+str(i)+'Brackets']['winrate']=(numOfWinsTotal/(numOfWinsTotal+numOfLossesTotal))*100
                print(f"Tier{i}Average Placement: {avgPlacement}, Record: {numOfWinsTotal}-{numOfLossesTotal}")
            allWins+=numOfWinsTotal
            allLosses+=numOfLossesTotal
        playerData['record']=str(allWins)+"-"+str(allLosses)
        playerData['winrate']=(allWins/(allWins+allLosses))*100
        if numOfUniqueBrackets >= 3 and playerData['eligible']:
            playerData['eligible'] = True
        else:
            playerData['eligible'] = False'''
        for wins in playerData['wins']:
            '''noteable = df[df['tag'] == wins['tag']]
            if not noteable.empty:
                winData = noteable.iloc[0].to_dict()
                winData['numOfWins'] = wins['numOfWins']
                playerData['noteableWins'].append(winData)'''
            lumirank = dfLumi[dfLumi['tag'] == wins['tag']]
            if not lumirank.empty:
                winData = lumirank.iloc[0].to_dict()
                capOrFact = do_verification(winData['id'], wins['winnerId'])
                if capOrFact:
                    winData['numOfWins'] = wins['numOfWins']
                    playerData['noteableWins'].append(winData)
with open('playersTest.json', 'w') as file:
      json.dump(data, file, indent=2)