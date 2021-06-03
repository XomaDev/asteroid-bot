import logging

from os import path
import telegram
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import better_profanity

from configparser import ConfigParser
import bingfo
import chocolateo
import commandscrape
import functions
from texttoaudio import toAudio

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
script_url = ''

def start(update: telegram.Update, _: CallbackContext) -> None:
    text = 'I am an intelligent bot for web-scrapping, finding/searching info and more! Join @AsteroidDiscuss for ' \
           'news and updates!\n\nControl me by these commands:\n\n/echo - replies the text ' \
           'back\n/answerx  - searches ' \
           'for related website/info on the internet ' \
           'with the given text\n/info ' \
           '- find info about someone or ' \
           'something\n/scrape - ' \
           'helps you scrape the web by ' \
           'commands\n/audio - converts the text ' \
           'to audio file\n\n Have fun using me! 😄\n' \
           'Ⴆყ 𝗖𝗼𝗹𝗼𝗿𝗖𝘂𝗯𝗲𝘀'
    update.message.reply_text(text)


def help_command(update: telegram.Update, _: CallbackContext) -> None:
    update.message.reply_text('Help!')


def echo(update: telegram.Update, _: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def filterText(update: telegram.Update, _: CallbackContext) -> None:
    try:
        if better_profanity.profanity.contains_profanity(update.message.text):
            update.message.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
    except:
        pass


def texttoaudio(update: telegram.Update, _: CallbackContext) -> None:
    try:
        text = update.message.text[7:]
        if not better_profanity.profanity.contains_profanity(update.message.text):
            update.message.bot.sendAudio(update.message.chat_id, toAudio(text), title="asteroid.mp3",
                                         caption=update.message.from_user.username)
    except Exception:
        pass


def answer(update: telegram.Update, _: CallbackContext) -> None:
    if len(update.message.text) > 9:
        question = update.message.text[9:]
        update.message.bot.send_chat_action(update.message.chat.id, 'typing')

        if " ".join(functions.checkForURLs(question)) == question:
            update.message.reply_text('I cannot search for just URL! Add some keywords or tags!')
        else:
            result = chocolateo.web_scrape(question)

            if result[1] != "":
                if result[0] != "":
                    buttons = [[telegram.InlineKeyboardButton(text="More info", url=result[1])]]

                    keyboard = telegram.InlineKeyboardMarkup(buttons)
                    update.message.bot.sendMessage(update.message.chat_id, text=functions.enhanceText(result[0]),
                                                   reply_markup=keyboard)
            else:
                text = result[0] + "\n\n" + result[1]
                update.message.reply_text(text)


def info(update: telegram.Update, _: CallbackContext) -> None:
    try:
        i = update.message.text
        result = chocolateo.bingScrape(i[6:])
        update.message.reply_text(result)
    except:
        pass


def delete(update: telegram.Update, _: CallbackContext) -> None:
    try:
        update.message.bot.deleteMessage(chat_id=update.message.chat.id,
                                         message_id=update.message.reply_to_message.message_id)
        update.message.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
    except:
        pass


def base64(update: telegram.Update, _: CallbackContext) -> None:
    try:
        update.message.reply_text(functions.encode(update.message.text[8:]))
    except:
        pass


def commandScrape(update: telegram.Update, _: CallbackContext) -> None:
    result = commandscrape.command_scrape(update.message.text[8:])
    parseMode = 'MarkdownV2'


    if result[1] == -1:
        update.message.reply_text(result[0])
    else:
        update.message.reply_text(result[0], parse_mode=parseMode)

def short(update: telegram.Update, _: CallbackContext) -> None:
    if script_url != '':
        target_site = update.message.text[7:]

        if not target_site.startswith('http'):
            target_site = 'http://' + target_site

        target_location = 'https://script.google.com/macros/s/' + script_url + '/exec?url=' + target_site

        web_request = request.Request(target_location)
        response = request.urlopen(web_request).read()
        decodedResponse = response.decode(DECODING_FORMAT)

        if decodedResponse[0:len('Awesome')] == 'Awesome':  # Check ff it's successful
            update.message.reply_text(decodedResponse)
        else:
            update.message.reply_text('Error: \n' + decodedResponse)

def main() -> None:
    """Start the bot."""
    # parsing config.ini file
    config = ConfigParser()
    if not path.isfile('config.ini'):
        printf("Missing config.ini file... exiting.")
        exit(-1)

    config.read('config.ini')
    api_id = config['AUTH']['API_ID']
    api_hash = config['AUTH']['API_HASH']
    bot_token = comnfig['AUTH']['bot_token']

    if bot_token == "DUMMY":
        print("Bot token missing in config.ini file... exiting.")
        exit(-1)
        

    # Create the Updater and pass it your bot's token.
    updater = Updater(bot_token) # BOT TOKEN

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("answerx", answer))
    dispatcher.add_handler(CommandHandler("delete", delete))
    dispatcher.add_handler(CommandHandler("base64", base64))
    dispatcher.add_handler(CommandHandler("info", info))
    dispatcher.add_handler(CommandHandler("audio", texttoaudio))
    dispatcher.add_handler(CommandHandler("scrape", commandScrape))
    dispatcher.add_handler(CommandHandler("short", short))
    dispatcher.add_handler(CommandHandler("echo", echo))
    

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, filterText))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
