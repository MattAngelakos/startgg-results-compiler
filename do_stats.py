import json
import pandas as pd
f = open('playersTest.json')
data = json.load(f)
df = pd.read_csv('oor.csv')
for player, playerData in data.items():
    if(playerData['eligible']):
        print(player)
        """allWins = 0
        allLosses = 0
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
                        #print("Wins:")
                        for wins in tiertourneyData['wins']:
                            numOfWins+=wins['numOfWins']
                            #print(f"{wins['tag']}(x{wins['numOfWins']})")
                        #print("Losses:")
                        for losses in tiertourneyData['losses']:
                            numOfLosses+=losses['numOfLosses']
                            #print(f"{wins['tag']}(x{wins['numOfLosses']})")
                        print(f"Tournery: {tiertourney}, Placement: {tiertourneyData['placement']}, Record: {numOfWins}-{numOfLosses}")
                        avgPlacement += tiertourneyData['placement']
                        numOfBrackets+=1
                        numOfWinsTotal+=numOfWins
                        numOfLossesTotal+=numOfLosses
                        tiertourneyData['record']=str(numOfWins)+"-"+str(numOfLosses)
            if numOfBrackets:
                avgPlacement = avgPlacement/numOfBrackets
                playerData['Tier'+str(i)+'Brackets']['avgPlacement']=avgPlacement
                playerData['Tier'+str(i)+'Brackets']['record']=str(numOfWinsTotal)+"-"+str(numOfLossesTotal)
                playerData['Tier'+str(i)+'Brackets']['winrate']=(numOfWinsTotal/(numOfWinsTotal+numOfLossesTotal))*100
                print(f"Tier{i}Average Placement: {avgPlacement}, Record: {numOfWinsTotal}-{numOfLossesTotal}")
            allWins+=numOfWinsTotal
            allLosses+=numOfLossesTotal
        playerData['record']=str(allWins)+"-"+str(allLosses)
        playerData['winrate']=(allWins/(allWins+allLosses))*100"""
        for wins in playerData['wins']:
            noteable = df[df['tag'] == wins['tag']]
            if not noteable.empty:
                 winData = noteable.iloc[0].to_dict()
                 winData['numOfWins'] = wins['numOfWins']
                 playerData['noteableWins'].append(winData)
with open('playersTest.json', 'w') as file:
      json.dump(data, file, indent=2)