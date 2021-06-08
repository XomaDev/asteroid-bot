import random
import re
from urllib import request

import nltk
from nltk.corpus import words
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob

from info import USER_AGENT

nltk.download('words')

wordNetLemmatizer = WordNetLemmatizer()

file = open('non-code-files/filtered-emojis.txt', 'rb')
emoji_values = file.read().decode().splitlines()
file.close()

emojis = []
emoji_text = []

for line in emoji_values:
    text1 = line.split(' ')

    emojis.append(text1[0])
    emoji_text.append(text1[1])


def replaceSpaceEmojis(choice, text):
    if ' ' in text:
        textRes = str(text).replace(' ', random.choice(choice), 1)
    else:
        textRes = str(text) + ' ' + random.choice(choice)
    return textRes


def withEmojis(text):
    words = text.split(" ")

    result = 0
    texztRes = ''

    for feedback in words:
        feedback_polarity = TextBlob(feedback).sentiment.polarity

        result = result + feedback_polarity

    positiveEmojis = '😀 😃 😄 😁 ☺️ ️😇 😊 🙂 🙃 😉 😌 😍 🥰  🥳 🤩 😎 🤓'.split(' ')
    moderateEmojis = '😮 😐 😑 😓 🤔 🤥 😯 🤫 😲 😮'.split(' ')
    negativeEmojis = '😧 🥺 😢 😭 😩 😩 😮 😦 😦 😣 😖 ☹ ️ 🙁 😕 😟 😔 😞 😰 😥 😨'.split(' ')

    if result > 0:
        textRes = replaceSpaceEmojis(positiveEmojis, text)
    elif result == 0:
        textRes = replaceSpaceEmojis(moderateEmojis, text)
    else:
        textRes = replaceSpaceEmojis(negativeEmojis, text)
    return textRes


def add_emojis(text):
    replace_target = ['-', '_', '=']

    for replace in replace_target:
        text = text.replace(replace, ' ')

    text_new = []

    for word in text.split(' '):
        text_new.append(word)
        new_word = re.sub(r"(\w)([A-Z])", r"\1 \2", word)

        can_pass = word in words.words()

        word = new_word

        if not can_pass:
            for segment in new_word.split(' '):
                segment = segment.lower()
                can_pass = segment in words.words()

        if can_pass:
            word = word.lower()
            word_stemmed = wordNetLemmatizer.lemmatize(word)

            for word1 in word_stemmed.split(' '):
                try:
                    i = emoji_text.index(word1)
                    text_new.append(emojis[i])
                except ValueError:
                    pass

    return ' '.join(text_new)


fruits = open('non-code-files/fruits.txt', 'r').read()
fruits = fruits.split('\n')
slaps_texts = 'https://raw.githubusercontent.com/XomaDev/asteroid-bot-dev/main/external_files/asteroid-slaps.txt'

web_request = request.Request(slaps_texts)
web_request.add_header("User-Agent", USER_AGENT)

response = request.urlopen(web_request).read().decode()


def slap(user, to):
    user = re.sub(r'[0-9]+', '', user)
    to = re.sub(r'[0-9]+', '', to)

    parts = response.split('-- ignore')
    is_first_selection = False

    if random.choice([1, 2]) == 1:
        slap_data = parts[0]
        is_first_selection = True
    else:

        slap_data = parts[1]

    choice_data = slap_data.split('\n')

    choice = random.choice(choice_data)
    if not is_first_selection:
        choice = 'You slap them with: ' + choice

    random_fruit = random.choice(fruits) + ' fruit'

    choice = choice.replace("<p>", user)
    choice = choice.replace("<t>", to)
    choice = choice.replace("<fruit>", random_fruit)
    choice = choice.replace("<r_num>", str(random.randint(0, 12)))

    return withEmojis(add_emojis(choice))
