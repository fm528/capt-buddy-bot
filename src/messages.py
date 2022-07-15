import config

MESSAGE_SENT = 'Message sent!\n(/send to send another!)'
HELP_TEXT = (
    'Use /send to send a message to your friend and /cancel to cancel message.'
    '\n\nThis bot supports forwarding only text, photos, stickers, documents, audio, video, and animations.'
)
ERROR_CHAT_ID = 'Sorry an error occured please type /start again.'
SEND_COMMAND = 'Send a message to your friend!\nUse /cancel to stop.'
NOT_REGISTERED = 'Sorry you are not registered with the game currently.'


def getBotNotStartedMessage(alias):
    return f'Sorry your {alias} has not started this bot'


def getPlayerMessage(alias):
    return f'Please type your message to your {alias}\n(/cancel to stop)'


def getReceivedMessage(alias, text=""):
    return f"Message from your {alias}:\n\n{text}" if text != "" else f"Message from your {alias}:"


def getSentMessageLog(alias, sender, receiver):
    return f'{sender} sent a message to their {alias} {receiver}'


def getNotRegisteredLog(alias, sender, receiver):
    return f'{sender} {alias} {receiver} has not started the bot'
