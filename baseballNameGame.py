'''
Baseball Name Game
Matthew Swanson
2020.07.03
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

source_filename = 'People.csv'

def parse():
    df = pd.read_csv(source_filename)
    df = df[['nameFirst', 'nameLast']]
    df = df.dropna()
    
    df['firstInit'] = df['nameFirst'].apply(lambda name: ord(name[0].upper()))
    df['lastInit'] = df['nameLast'].apply(lambda name: ord(name[0].upper()))
    
    df = df[['firstInit', 'lastInit']]
    return df

def play(df, debug):
    # Set up game
    pickedPlayers = []
    rounds = 0
    
    # Get first player
    player = df.sample(1)
    df = df.drop(player.index)
    pickedPlayers.append(player)
    numPossiblePlayers = len(df)
    rounds = rounds + 1

    # Game loop
    while True:
        if debug:
            print(str(rounds) + '\t'
                  + str(numPossiblePlayers) + '\t'
                  + player['firstInit'].to_string(index=False) + '\t'
                  + player['lastInit'].to_string(index=False))
        lastInit = player['lastInit'].values[0]
        possiblePlayers = df.loc[df['firstInit'] == lastInit]
        if possiblePlayers.empty:
            if debug:
                print(str(len(pickedPlayers)) + '\t'
                      + str(len(possiblePlayers)))
            return len(pickedPlayers)
        else:
            player = possiblePlayers.sample(1)
            df = df.drop(player.index)
            pickedPlayers.append(player)
            numPossiblePlayers = len(possiblePlayers)
            rounds = rounds + 1

def main():
    # Parse data
    df = parse()

    # Play games
    games = []
    numGames = 30
    for i in range(0,numGames):
        games.append(play(df=df.copy(), debug=False))
        print('Game ' + str(i+1) + ' of ' + str(numGames) + ' completed...')

    # Summarize games
    games.sort()
    print(games)
    plt.hist(games, bins=10, edgecolor='white')
    plt.show()

if __name__ == "__main__":
    main()
