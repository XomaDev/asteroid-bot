import logging

from urllib import request
import telegram
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import better_profanity

import chocolateo
import commandscrape
import functions
from info import DECODING_FORMAT
from texttoaudio import toAudio

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

script_url = 'AKfycbxJ2z8PwKW2BxLd3oMDUqI7JbcyqKUG9tOinKkTfrATE_lt8O2N'


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
    update.message.bot.send_chat_action(update.message.chat.id, 'record_voice')
    text = update.message.text[7:]
    if not better_profanity.profanity.contains_profanity(update.message.text):
        update.message.bot.sendAudio(update.message.chat_id, toAudio(text), title="asteroid.mp3",
                                     caption=update.message.from_user.username)


def answer(update: telegram.Update, _: CallbackContext) -> None:
    if len(update.message.text) > 9:
        question = update.message.text[9:]
        update.message.bot.send_chat_action(update.message.chat.id, 'typing')

        joined = " ".join(functions.checkForURLs(question))

        if joined == question:
            update.message.reply_text('I cannot search for just URL! Add some keywords or tags! If you believe this is '
                                      'a valid search, this keyword(s) may be not searchable.')
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
    update.message.bot.send_chat_action(update.message.chat.id, 'typing')
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


# def parse(update: telegram.Update, _: CallbackContext) -> None:
#     result = natural_language_parser.processText(update.message.text[7:])
#     print(result)
#     update.message.reply_text(result)



def slap(update: telegram.Update, _: CallbackContext) -> None:
    username = update.message.from_user.username

    try:
        target_user = update.message.reply_to_message.from_user.username
    except:
        update.message.reply_text('Reply to a message that I can slap!')
        return
    import slap
    update.message.reply_text(slap.slap(username, target_user))


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
    updater = Updater("1760053369:AAG7IPxbxrGHAJcNUqY60hAu3oiFao_8NRQ")

    dispatcher = updater.dispatcher

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
    dispatcher.add_handler(CommandHandler("slap", slap))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, filterText))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
