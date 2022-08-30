import pickle
import player
from collections import defaultdict

with open('C:/Users/fmcmu/Documents/GitHub/capt-buddy-bot/csv/players.txt', 'wb') as playersFile:
    players = defaultdict(player.Player)
    pickle.dump(players, playersFile)

