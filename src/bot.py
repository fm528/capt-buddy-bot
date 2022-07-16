import os
import player
import messages
import logging
import datetime
from collections import defaultdict
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler


PORT = int(os.environ.get('PORT', 5000))
BOT_TOKEN = os.environ['BOT_TOKEN']

# Enable logging.
logging.basicConfig(
    filename=f'../log/{datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")}.log',
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
            update.message.reply_text(messages.PARTNER_UNAVAILABLE)
        else:
            update.message.reply_text(messages.PARTNER_AVAILABLE)
            context.bot.send_message(
                text=messages.INFORM_PARTNER,
                chat_id=players[playerName].partner.chat_id
            )


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
    if not players[playerName].is_online or not players[playerName].partner.is_online:
        return
    if update.message.text:
        context.bot.send_message(
            text=update.message.text,
            chat_id=players[playerName].partner.chat_id
        )
    else:
        sendNonTextMessage(update.message, context.bot, players[playerName].partner.chat_id)


def end_command(update: Update, context: CallbackContext) -> None:
    # End convo when the command /end is issued.
    playerName = update.message.chat.username.lower()
    players[playerName].is_online = False
    logger.info(f"{update.message.chat.username} ended the conversation.")
    if players[playerName].partner.is_online:
        context.bot.send_message(
            text=messages.LEFT_CHAT,
            chat_id=players[playerName].partner.chat_id
        )
    update.message.reply_text('Sending message cancelled.')


def admin_command(update: Update, context: CallbackContext) -> None:
    # Display admin guide when the command /admin is issued.
    update.message.reply_text(messages.ADMIN_GUIDE)


def upload_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Saved file.')
    with open('./inputs/pairings.csv', 'wb+') as csv_file:
        context.bot.get_file(update.message.document).download(out=csv_file)
    reload_command(update, CallbackContext)


def reload_command(update: Update, context: CallbackContext) -> None:
    # Reload database after receiving new csv file.
    update.message.reply_text(player.loadPlayers(players))
    update.message.reply_text('Players reloaded successfully.')
    logger.info('Players reloaded with new csv file.')


def reset_command(update: Update, context: CallbackContext) -> None:
    # Reset database when the command reset is issued.
    players.clear()
    if os.path.exists('./inputs/pairings.csv'):
        os.remove('./inputs/pairings.csv')
        logger.info('Pairings.csv has been removed.')
    else:
        logger.info('Pairings.csv not found.')
    update.message.reply_text('Players have been resetted.')
    logger.info('Players have been resetted.')


def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # User commands
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("chat", chat_command))
    dispatcher.add_handler(MessageHandler(~Filters.command & ~Filters.document.file_extension("csv"), sendMsg))
    dispatcher.add_handler(CommandHandler("end", end_command))

    # Admin commands.
    dispatcher.add_handler(CommandHandler("admin", admin_command))
    dispatcher.add_handler(CommandHandler("reset", reset_command))
    dispatcher.add_handler(MessageHandler(Filters.document.file_extension("csv"), upload_command))

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=BOT_TOKEN)
    updater.bot.setWebhook('https://capt-buddy-bot.herokuapp.com/' + BOT_TOKEN)
    # updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    try:
        logger.info("Bot has started.")
        main()
    finally:
        logger.info("Bot has terminated.")
