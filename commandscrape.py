from urllib import request
from urllib.error import HTTPError

from bs4 import BeautifulSoup

from info import USER_AGENT, DECODING_FORMAT, HTML_PARSE_FORMAT


def command_scrape(commandsText):
    commands = commandsText.split("\n")

    URL_COMMAND = commands[0] + ""

    if not URL_COMMAND.startswith("from "):
        return ["The first command should contain the URL example:\n'from FULL_URL'", -1]

    URL_SPLIT = commands[0].split("from ")

    if len(URL_SPLIT) > 0:
        TARGET_URL = commands[0].split("from ")[1]
    else:
        return ['No URL found or the URL provided is invalid', -1]

    try:
        web_request = request.Request(TARGET_URL)
    except ValueError:
        return ['The URL provided is invalid. Enter a valid full URL.', -1]

    web_request.add_header("User-Agent", USER_AGENT)

    try:
        response = request.urlopen(web_request).read()
    except HTTPError:
        return ['The site is not valid or the page docent exists', -1]

    decodedResponse = response.decode(DECODING_FORMAT)

    bsSoup = BeautifulSoup(decodedResponse, HTML_PARSE_FORMAT)

    result = ''

    i = 0
    for command in commands:
        text = command
        try:
            if not i == 0:
                if command[0] == ' ':
                    command = command[1:]
                if command.startswith("->"):
                    index = command.split('!')[0][2:]
                    command = command.split('!')[1]
                    result = result + '```\n' + findData(bsSoup, command, True)[int(index) - 1].getText() + '\n```'
                elif command.startswith(">"):
                    command = command[2:]
                    result = result + '```\n' + findData(bsSoup, command, False) + '\n```'
                else:
                    result = 'Invalid command at line:  ' + str(i + 2)
                    break
            i = i + 1
        except IndexError:
            result = 'Index provided is out of range\\ at line: ' + str(i + 2) + ' for command: \n`' + text + '`'
            break

    return [result, 1]


def findData(bsSoup, command, toFindAll):
    data = command.strip().split(" ")

    elementType = data[0]
    attributeName = data[1]
    attributeValue = data[2]

    if attributeName == '-n':
        attributeName = ''
    if attributeValue == '-n':
        attributeValue = ''

    if not toFindAll:
        findValue = bsSoup.find(elementType, {attributeName: attributeValue})

        if findValue is None:
            return 'An error occurred'
        else:
            return findValue.getText()
    else:
        return bsSoup.find_all(elementType, {attributeName: attributeValue})
