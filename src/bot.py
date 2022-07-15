import logging
import player
import messages
import datetime
from collections import defaultdict

import config

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler, CallbackQueryHandler


# Enable logging.
logging.basicConfig(
    filename=f'log/{datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")}.log',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialise players.
# Default value for the dictionary is a new Player object.
players = defaultdict(player.Player)
player.loadPlayers(players)


def start_command(update: Update, context: CallbackContext) -> None:
    # Send a message when the command /start is issued.
    playerName = update.message.chat.username.lower()
    if players[playerName].username is None:
        # Player not found/ registered.
        update.message.reply_text(messages.NOT_REGISTERED)
        return
    # Register chat id for message sending.
    players[playerName].chat_id = update.message.chat.id
    logger.info(f'{playerName} started the bot with chat_id {players[playerName].chat_id}.')
    update.message.reply_text(f'Hey {playerName}! {messages.HELP_TEXT}')


def help_command(update: Update, context: CallbackContext) -> None:
    # Send a message when the command /help is issued.
    update.message.reply_text(messages.HELP_TEXT)


def reload_command(update: Update, context: CallbackContext) -> None:
    # Send a message when the command /reloadplayers is issued.
    player.saveChatID(players)
    logger.info(f'Player chat ids have been saved in {config.CHAT_ID_JSON}.')
    player.loadPlayers(players)
    logger.info(f'Players reloaded.')
    update.message.reply_text(f'Players reloaded.')


def chat_command(update: Update, context: CallbackContext):
    # Start send convo when the command /chat is issued
    playerName = update.message.chat.username.lower()
    if players[playerName].username is None:
        # Player not found/ registered.
        update.message.reply_text(messages.NOT_REGISTERED)
        return ConversationHandler.END
    if players[playerName].chat_id is None:
        # Player chat id not found.
        update.message.reply_text(messages.ERROR_CHAT_ID)
        return ConversationHandler.END
    if not players[playerName].is_online:
        players[playerName].is_online = True
        if not players[playerName].partner.is_online:
            update.message.reply_text('You are now online but your friend has not started the chat.')
        else:
            update.message.reply_text('You are now online and connected to your friend.')


def sendNonTextMessage(message, bot, chat_id):
    if message.photo:
        bot.send_photo(
            photo=message.photo[-1],
            caption=message.caption,
            chat_id=chat_id
        )
    elif message.sticker:
        bot.send_sticker(
            sticker=message.sticker,
            chat_id=chat_id
        )
    elif message.document:
        bot.send_document(
            document=message.document,
            caption=message.caption,
            chat_id=chat_id
        )
    elif message.video:
        bot.send_video(
            video=message.video,
            caption=message.caption,
            chat_id=chat_id
        )
    elif message.video_note:
        bot.send_video_note(
            video_note=message.video_note,
            chat_id=chat_id
        )
    elif message.voice:
        bot.send_voice(
            voice=message.voice,
            chat_id=chat_id
        )
    elif message.audio:
        bot.send_audio(
            audio=message.audio,
            chat_id=chat_id
        )
    elif message.animation:
        bot.send_animation(
            animation=message.animation,
            chat_id=chat_id
        )


def sendMsg(update: Update, context: CallbackContext):
    playerName = update.message.chat.username.lower()
    if not players[playerName].is_online:
        return
    if update.message.text:
        context.bot.send_message(
            text=update.message.text,
            chat_id=players[playerName].partner.chat_id
        )
    else:
        sendNonTextMessage(update.message, context.bot, players[playerName].partner.chat_id)
    # logger.info(messages.getSentMessageLog(config.ANGEL_ALIAS, playerName, players[playerName].angel.username))


def end_command(update: Update, context: CallbackContext) -> int:
    # End convo when the command /end is issued.
    playerName = update.message.chat.username.lower()
    players[playerName].is_online = False
    logger.info(f"{update.message.chat.username} canceled the conversation.")
    context.bot.send_message(
        text="Your friend has ended the conversation.",
        chat_id=players[playerName].partner.chat_id
    )
    update.message.reply_text(
        'Sending message cancelled.'
    )


def main():
    # Start the bot.
    updater = Updater(config.ANGEL_BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers.
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("chat", chat_command))
    dispatcher.add_handler(CommandHandler("reload", reload_command))
    dispatcher.add_handler(CommandHandler("end", end_command))
    dispatcher.add_handler(MessageHandler(sendMsg))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    try:
        main()
    finally:
        player.saveChatID(players)
        logger.info(f'Player chat ids have been saved in {config.CHAT_ID_JSON}')
