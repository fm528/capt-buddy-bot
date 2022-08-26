WELCOME_TEXT = 'You will now join the conversation with your buddy! The conversation will only start when both sides have started the bot.\n\n'
HELP_TEXT = (
    'This bot supports only text, photos, stickers, documents, audio, video, and animations.'
    '\n\nThe messages between you and buddy will not be recorded. The conversation will automatically end after the event.'
    '\n\nUse /help if you want to see this message again.'
)
ERROR_CHAT_ID = 'Sorry an error occured please type /start again.'
NOT_REGISTERED = 'Sorry you are not registered with the bot currently.'
PARTNER_UNAVAILABLE = 'You have started the chat but your buddy has not joined.'
PARTNER_AVAILABLE = 'You have joined the chat and are now chatting with your buddy.'
INFORM_PARTNER = 'Your buddy has joined the chat.'
ADMIN_GUIDE = (
    '*FOR ADMIN USERS ONLY*\n\nFollow these steps to upload your pairings:\n\n'
    '1\) Open the `sample\.csv` file using Notepad \(Windows\) or TextEdit \(Mac\)\n'
    '2\) Do not change the first line\n'
    '3\) From the second line onwards, enter the pairing in the format `@telehandle1,@telehandle2`\n'
    '4\) Once done, save the file\n'
    '5\) Send the file to me and I\'ll process it\n\n'
    'Do not that this will override any previous pairings\. Use /reset to clear pairing and /reload to refresh the pairings\.'
)
