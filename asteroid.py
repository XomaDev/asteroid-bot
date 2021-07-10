import logging

from os import path
import telegram
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import better_profanity

from configparser import ConfigParser
import bingfo
import chocolateo
import exifextract
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
           'back\n/answer  - searches ' \
           'for related website/info on the internet ' \
           'with the given text\n/info ' \
           '- find info about someone or ' \
           'something\n/scrape - ' \
           'helps you scrape the web by ' \
           'commands\n/audio - converts the text\n' \
           '/base64 - converts text to base 64\n' \
           "/short - shorts the URL using Peico's service\n" \
           '/slaps - slaps the user using some funny sentences\n' \
           '/exif - extract the exif data from images files sent uncompressed\n' \
           '/emote - to know the sentiment recognition of a text through emojis\n' \
           '/quote - tells a random thought or quote\n' \
           'to audio file\n\n Have fun using me! 😄\n' \
           'Ⴆყ 𝗖𝗼𝗹𝗼𝗿𝗧𝗵𝗶𝗻𝗴𝘀'
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

    
def answerx(update: telegram.Update, _: CallbackContext) -> None:
    update.message.reply_text('/answerx command is deprecated! Use /answer command!')
    
    

def answer(update: telegram.Update, _: CallbackContext) -> None:
    try:
        question = update.message.text
        result = chocolateo.web_scrape(question[9:])

        if result[1] != "":
            if result[0] != "":
                buttons = [[telegram.InlineKeyboardButton(text="More info", url=result[1])]]

                keyboard = telegram.InlineKeyboardMarkup(buttons)
                update.message.bot.sendMessage(update.message.chat_id, text=functions.enhanceText(result[0]),
                                               reply_markup=keyboard)
        else:
            text = result[0] + "\n\n" + result[1]
            update.message.reply_text(text)
    except:
        pass


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
    
def quote(update: telegram.Update, _: CallbackContext) -> None:
    target_url = 'https://api.quotable.io/random'
    req = requests.get(target_url)
    if req.status_code == 200:
        result = req.text
        result1 = json.loads(result)

        quote1 = functions.replace_special_slash(result1['content'])
        author = functions.replace_special_slash(result1['author'])

        update.message.reply_markdown_v2(quote1 + '\n\n' + '\- ' + functions.stylish_text(author))
    else:
        update.message.reply_text('I could not find any thoughts!') 
    
def exif_data(update: telegram.Update, _: CallbackContext) -> None:
    uncompressed_message = 'Reply to a message with an image sent uncompressed. Else the replied message do ' \
                           'not have any image file.'

    try:
        document = update.message.reply_to_message.document
    except:
        update.message.reply_text(uncompressed_message)
        return ()

    supported_formats = ['jpg', 'jpeg', 'png']

    if document is not None:
        is_supported = False

        for image_format in supported_formats:
            if document.file_name.endswith('.' + image_format):
                is_supported = True
                break

        if is_supported:
            try:
                text = exifextract.extractMetaFromURL(document.get_file().file_path)
                update.message.reply_text(text)
            except:
                update.message.reply_text('There is no meta data found!')
        else:
            update.message.reply_text('The given file format is not supported. The supported formats are PNG, '
                                      'JPG and JPEG')
    else:
        update.message.reply_text(uncompressed_message)
        
def emote(update: telegram.Update, _: CallbackContext) -> None:
    text = update.message.text

    try:
        if not len(text) > 7:
            text = update.message.reply_to_message.text
            text = text[7:]
    except:
        update.message.reply_text('I could not find any message replied or add some text after the command.')
        return ()
    try:
        import slap
        update.message.reply_text(slap.withEmojis(text))
    except:
        update.message.reply_text('I could not add emotes!')

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
        print("Missing config.ini file... exiting.")
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
    dispatcher.add_handler(CommandHandler("answerx", answerx))
    dispatcher.add_handler(CommandHandler("answer", answer))
    dispatcher.add_handler(CommandHandler("delete", delete))
    dispatcher.add_handler(CommandHandler("base64", base64))
    dispatcher.add_handler(CommandHandler("info", info))
    dispatcher.add_handler(CommandHandler("audio", texttoaudio))
    dispatcher.add_handler(CommandHandler("scrape", commandScrape))
    dispatcher.add_handler(CommandHandler("short", short))
    dispatcher.add_handler(CommandHandler("exif", exif_data))
    dispatcher.add_handler(CommandHandler("emote", emote))
    dispatcher.add_handler(CommandHandler("quote", quote))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, filterText))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
