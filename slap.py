import random
import re
from urllib import request

from info import USER_AGENT


fruits = open('non-code-files/fruits.txt', 'r').read()
fruits = fruits.split('\n')
slaps_texts = 'https://raw.githubusercontent.com/XomaDev/asteroid-bot-dev/main/external_files/asteroid-slaps.txt'


def slap(user, to):
    user = re.sub(r'[0-9]+', '', user)
    to = re.sub(r'[0-9]+', '', to)

    web_request = request.Request(slaps_texts)
    web_request.add_header("User-Agent", USER_AGENT)

    response = request.urlopen(web_request).read().decode()

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

    return choice
