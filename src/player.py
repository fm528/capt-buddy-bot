import config
import csv
import json
import logging

logger = logging.getLogger(__name__)


class Player():
    def __init__(self):
        self.username = None
        self.angel = None
        self.mortal = None
        self.chat_id = None


# Initialise dict of players from players file
def loadPlayers(players: dict):
    with open(config.PLAYERS_FILENAME) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                logger.info(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                playerName = row[0].strip().lower()
                partnerName = row[1].strip().lower()
                logger.info(f'\t{playerName} has partner {partnerName}.')
                players[playerName].username = playerName
                players[playerName].partner = players[partnerName]
                players[playerName].is_online = False
                line_count += 1
        logger.info(f'Processed {line_count} lines.')
    validatePairings(players)
    loadChatID(players)


# Checks if players relation is symmetric
def validatePairings(players: dict):
    for _, player in players.items():
        if player.partner.partner.username != player.username:
            print(f'Error with {player.username} pairings')
            logger.error(f'Error with {player.username} pairings')
            exit(1)
    logger.info(f'Validation complete, no issues with pairings.')


def saveChatID(players: dict):
    chatDict = {}
    for k, v in players.items():
        chatDict[k] = v.chat_id
    with open(config.CHAT_ID_JSON, 'w+') as f:
        json.dump(chatDict, f)


def loadChatID(players: dict):
    try:
        with open(config.CHAT_ID_JSON, 'r') as f:
            chatDict = json.load(f)
            logger.info(chatDict)
            for k, v in chatDict.items():
                players[k].chat_id = v
    except:
        logger.warn('Fail to load chat ids')
