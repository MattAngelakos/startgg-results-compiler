import json
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table
from matplotlib.table import Table
f = open('playersTest.json')
data = json.load(f)
df = pd.read_csv('h2h.csv')
for tag in data:
    df[tag] = tag
for tag in data:
    new_row = {'tag': tag} 
    df = df._append(new_row, ignore_index=True)
print(df)
df.to_csv('h2h.csv', index=False)
for index, row in df.iterrows():
    tag = row.iloc[0]
    for opponent, h2h in zip(df.columns[1:], row.iloc[1:]):
        if opponent != tag:
            try:
                matching_entry_wins = next(entry for entry in data[tag]['wins'] if entry['tag'] == opponent)
                numOfWins = matching_entry_wins['numOfWins']
            except:
                numOfWins = 0
            try:
                matching_entry_losses = next(entry for entry in data[tag]['losses'] if entry['tag'] == opponent)
                numOfLosses = matching_entry_losses['numOfLosses']
            except:
                numOfLosses = 0
            newH2H = str(numOfWins)+"-"+str(numOfLosses)
            df.at[index, opponent] = newH2H
df = df.astype(object)
df.to_csv('h2h.csv', index=False)
def color_cells(h2h):
    if h2h != h2h:
        return "black"
    parts = str(h2h).split("-")
    score0 = int(parts[0])
    score1 = int(parts[1])
    if score0 > score1:
        return "mediumseagreen"
    elif score1 > score0:
        return "tomato"
    else:
        return "gold"
    





fig, ax = plt.subplots()
ax.axis('off')
# Plot the DataFrame as a table with colored cells
tab = table(ax, df, loc='center', cellLoc='center', colWidths=[0.2]*len(df.columns))

for key, cell in tab.get_celld().items():
    if key[0] == 0:
        cell.set_text_props(weight='bold')
        cell.set_facecolor('lightgray')
    else:
        i, j = key
        cell_val = df.iat[i - 1, j]
        cell.set_text_props(weight='bold')
        if i != 0 and j != 0:
            cell.set_facecolor(color_cells(cell_val))
        else:
            cell.set_facecolor('lightgray')

# Show the table
plt.show()