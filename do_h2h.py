import json
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table
from matplotlib.table import Table
import re
def do_the_h2h(playerJson, h2hcsv):
    f = open(playerJson)
    data = json.load(f)
    df = pd.read_csv(h2hcsv)
    for tag in data:
        #if data[tag]['eligible']:
            df[tag] = tag
    for tag in data:
        #if data[tag]['eligible']:
            new_row = {'tag': tag} 
            df = df._append(new_row, ignore_index=True)
    df.to_csv(h2hcsv, index=False)
    def add(data, tag, opponent):
        try:
            matching_entry_wins = next(entry for entry in data[tag]['wins'] if entry['tag'] == opponent)
            numOfWins = matching_entry_wins['numOfWins']
        except:
            numOfWins=0
        try:
            matching_entry_losses = next(entry for entry in data[tag]['losses'] if entry['tag'] == opponent)
            numOfLosses = matching_entry_losses['numOfLosses']
        except:
            numOfLosses=0
        return numOfWins,numOfLosses
    print(df)
    for index, row in df.iterrows():
        tag = row.iloc[0]
        print(tag)
        for opponent, h2h in zip(df.columns[1:], row.iloc[1:]):
            if opponent != tag:
                numOfWins, numOfLosses = add(data, tag, opponent)
                print(opponent, numOfWins)
                for alt in data[opponent]['altTags']:
                    if opponent not in alt:
                        numOfWinsAlt, numOfLossesAlt = add(data, tag, alt)
                        numOfWins+=numOfWinsAlt
                        numOfLosses+=numOfLossesAlt
                newH2H = str(numOfWins)+"-"+str(numOfLosses)
                df.at[index, opponent] = newH2H
    print(df)
    df.to_csv(h2hcsv, index=False)
    first_col = df['tag']
    sorted_cols_df = df.drop(columns=['tag'])
# Function to extract the total number of losing h2hs from a col
    def calculate_h2hs_difference(col):
        if pd.notna(col):
            winning_count, losing_count = find_h2hs(col)
            if(winning_count > losing_count):
                return 1
            elif(winning_count < losing_count):
                return -1
            else:
                return 0
        return 0

    def find_h2hs(cell):
        h2hs = re.findall(r'(\d+)-(\d+)', cell)
        winning_count = sum(int(win[0] > win[1]) for win in h2hs)
        losing_count = sum(int(loss[0] < loss[1]) for loss in h2hs)
        return winning_count,losing_count

# Calculate the total number of losing h2hs for each column
    losing_h2hs_counts = sorted_cols_df.map(calculate_h2hs_difference).sum()
    print(losing_h2hs_counts)
# Reorder columns based on the total number of losing h2hs
    sorted_columns = losing_h2hs_counts.sort_values().index.tolist()
    print(sorted_columns)
    sorted_cols_df = sorted_cols_df[sorted_columns]
# Function to calculate the difference between winning and losing h2hs for a row
    def calculate_h2hs_difference(row):
        winloss_count = 0
        for cell in row:
            if pd.notna(cell):
                winning_count, losing_count = find_h2hs(cell)
                if(winning_count > losing_count):
                    winloss_count-=1
                elif(winning_count < losing_count):
                    winloss_count+=1
        return winloss_count
# Calculate the difference between winning and losing h2hs for each row
    h2hs_difference = sorted_cols_df.apply(calculate_h2hs_difference, axis=1)
    print(h2hs_difference)
# Reorder rows based on the difference between winning and losing h2hs
    sorted_rows = h2hs_difference.sort_values().index.tolist()
    sorted_cols_df = sorted_cols_df.loc[sorted_rows]
    sorted_cols_df.insert(0, 'tag', first_col)
    sorted_cols_df.reset_index(drop=True, inplace=True)
    df = sorted_cols_df
    df = df.astype(object)
    #df.to_csv(h2hcsv, index=False)
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
        elif score1 == score0 and score1 != 0:
            return "gold"
        else:
            return "lightgray"
    
    fig, ax = plt.subplots(figsize=(20,12))
    ax.axis('off')
# Plot the DataFrame as a table with colored cells
    tab = table(ax, df, loc='center', cellLoc='center', colWidths=[0.028]*len(df.columns))
    tab.auto_set_font_size(False)
    tab.set_fontsize(5)
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
def do_lumi():
    df = pd.read_csv('lumirank.csv')
    for index, row in df.iterrows():
        df.at[index, 'rank'] = int(index+1)
        df.at[index, 'region'] = 'lumirank'
    df['rank'] = df['rank'].astype(int)
    df.to_csv('lumirank.csv', index=False)
