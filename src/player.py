from unittest import result
import config
import csv
import json
import logging

logger = logging.getLogger(__name__)


class Player():
    def __init__(self):
        self.username = None
        self.partner = None
        self.chat_id = None
        self.is_online = False


# Initialise dict of players from players file
def loadPlayers(players: dict) -> str:
    players.clear()
    results = ""
    with open('./inputs/pairings.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                logger.info(f'Column names are {", ".join(row)}.')
                results += f'Column names are {", ".join(row)}.\n'
                line_count += 1
            else:
                playerName = row[0].strip().lower()
                partnerName = row[1].strip().lower()
                players[playerName].username = playerName
                players[playerName].partner = players[partnerName]
                logger.info(f'{playerName} has partner {partnerName}.')
                results += f'\n{playerName} has partner {partnerName}.'
                line_count += 1
        logger.info(f'Processed {line_count} lines.')
        results += f'\n\nProcessed {line_count} lines.\n'
    results += validatePairings(players)
    return results


# Checks if players relation is symmetric
def validatePairings(players: dict) -> str:
    for _, player in players.items():
        if player.partner.partner.username != player.username:
            print(f'Error with {player.username} pairings')
            logger.error(f'Error with {player.username} pairings')
            exit(1)
    logger.info('Validation complete, no issues with pairings.')
    return 'Validation complete, no issues with pairings.'
