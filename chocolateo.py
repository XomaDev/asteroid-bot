# Requirements:
#
# - URLLIB
# - BeautifulSoup
# - LXML


from urllib import request
from urllib.parse import quote

from bs4 import BeautifulSoup

import functions
from functions import stylish_text
from info import USER_AGENT, DECODING_FORMAT, HTML_PARSE_FORMAT

SEARCH_URL = "https://www.google.com/search?q="
BING_SEARCH_URL = "https://www.bing.com/search?q="

no_search_result = 'Your search keywords did not match any results.\n\n- Make sure that all words are spelled ' \
                   'correctly.\n- Try different keywords.\n- Try more general keywords. '

# Wikipedia values

WIKI_RESULT_TAG = "ruhjFe NJLBac fl"
WIKI_RESULT_TYPE = "a"
WIKI_FINAL_RESULT_TAG = "kno-rdesc"
WIKI_FINAL_RESULT_TYPE = "div"
WIKI_HEADING_TYPE = "h2"
WIKI_HEAD_TAG = "qrShPb"

# Dictionary values

DICTIONARY_EXAMPLE_EXTRA_TYPE = "div"
DICTIONARY_EXAMPLE_TAG = "H9KYcb"
DICTIONARY_EXTRA_TAG = "qFRZdb"
DICTIONARY_MEANING_TYPE = "div"
DICTIONARY_MEANING_TAG = "LTKOO sY7ric"
DICTIONARY_TITLE_TAG = "RjReFf"
DICTIONARY_TITLE_TYPE = 'div'
DICTIONARY_TAGS_TAG = 'ibnC6b'
DICTIONARY_TAGS_TYPE = 'div'
# Search results

SEARCH_RESULT_TYPE = "span"
SEARCH_RESULT_TAG = "aCOpRe"
SEARCH_RESULT_TAG1 = "IsZvec"
SEARCH_MATCH_TYPE = "cite"
SEARCH_MATCH_TAG = "iUh30 Zu0yb qLRx3b tjvcx"

SEARCH_TAG_NUM_TYPE = 'div'
SEARCH_TAG_NUM_TAG = 'result-stats'


def web_scrape(text):
    FINAL_RESULT = ""
    MATCH_SOURCE_NAME = ""

    targetURL = SEARCH_URL + quote(text, safe='')

    web_request = request.Request(targetURL)
    web_request.add_header("User-Agent", USER_AGENT)

    response = request.urlopen(web_request).read()
    decodedResponse = response.decode(DECODING_FORMAT)

    bsSoup = BeautifulSoup(decodedResponse, HTML_PARSE_FORMAT)

    soup = bsSoup

    # Wikipedia search

    for heading in \
            soup.select("h3"):
        heading.decompose()

    for tag in \
            soup.select(WIKI_RESULT_TYPE, {"class": WIKI_RESULT_TAG}):
        tag.decompose()

    wikipediaResult = soup.find(WIKI_FINAL_RESULT_TYPE,
                                {"class": WIKI_FINAL_RESULT_TAG})

    if str(wikipediaResult) != "None":
        FINAL_RESULT = wikipediaResult.getText()
        try:
            MATCH_SOURCE_NAME = "https://en.m.wikipedia.org/wiki/" + \
                                soup.find(WIKI_HEADING_TYPE, {"class": WIKI_HEAD_TAG}).getText().replace(" ", "_")
        except AttributeError:
            pass

    # Dictionary

    soup = bsSoup

    for tag in soup.find_all(DICTIONARY_EXAMPLE_EXTRA_TYPE,
                             {"class": DICTIONARY_EXAMPLE_TAG}):
        tag.decompose()

    for tag in soup.find_all(DICTIONARY_EXAMPLE_EXTRA_TYPE,
                             {"class": DICTIONARY_EXTRA_TAG}):
        tag.decompose()

    meanings = soup.find_all("div",
                             {"data-dobid": "dfn"})

    meanings_arranged = []

    for meaning in meanings:
        text = meaning.getText()
        text = text[0].upper() + text[1:]
        print(text)
        meanings_arranged.append(text)

    # print(meanings_arranged)

    if len(meanings_arranged) > 0:
        tags = []
        try:
            for tag in soup.find_all(DICTIONARY_TAGS_TYPE, {'jsname': DICTIONARY_TAGS_TAG, 'class': 'ArKEkc'}):
                tagText = tag.getText()
                if tagText != 'all':
                    tags.append(tag.getText())
            if len(tags) != 0:
                relatedTags = functions.stylish_text('[related-tags: ' + ', '.join(tags) + ']') + '\n'
            else:
                relatedTags = None
        except ValueError:
            relatedTags = '[tags: No tag found]'

        for meaning in meanings_arranged:
            FINAL_RESULT = FINAL_RESULT + "—  " + meaning + "\n\n"
        if len(meanings_arranged) == 1:
            FINAL_RESULT = FINAL_RESULT[2:]
        meaning_title = soup.find(DICTIONARY_TITLE_TYPE, {'class': "DgZBFd c8d6zd ya2TWb"})

        if relatedTags is None:
            relatedTags = ''

        try:
            FINAL_RESULT = '[𝗺𝗲𝗮𝗻𝗶𝗻𝗴: ' + functions.stylish_text(
                meaning_title.getText()) + ']\n' + relatedTags + '\n' + FINAL_RESULT
        except ValueError:
            FINAL_RESULT = '[𝗺𝗲𝗮𝗻𝗶𝗻𝗴]\n\n' + FINAL_RESULT

    # Search

    if len(FINAL_RESULT) == 0:
        can_proceed = True
        soup = bsSoup
        try:
            try:
                FINAL_RESULT = soup.find("div", {"class":"IsZvec"}).getText()
            except ValueError:
                FINAL_RESULT = soup.find(SEARCH_RESULT_TYPE, {"class": SEARCH_RESULT_TAG}).getText()
        except ValueError:
            try:
                FINAL_RESULT = soup.find('div', {"class": SEARCH_RESULT_TAG1}).getText()
            except ValueError:
                FINAL_RESULT = no_search_result
                can_proceed = False

        if not can_proceed:
            return [FINAL_RESULT, '']

        text = soup.find(SEARCH_MATCH_TYPE, {"class": SEARCH_MATCH_TAG}).getText()
        MATCH_SOURCE_NAME = text.replace(" › ", "/")

        newSoup = BeautifulSoup(decodedResponse, "lxml")

        children = newSoup.find("div", {"class": "tF2Cxc"}).findChildren("a")

        if children[0].get("href") != "":
            MATCH_SOURCE_NAME = (children[0].get("href"))

        if FINAL_RESULT == "":
            try:
                print(3)
                FINAL_RESULT = soup.find("div", {"class": "RqBzHd"}).getText()
            except:
                print(2)
                try:
                    FINAL_RESULT = soup.find("span", {"class": "hgKElc"}).getText()
                except:
                    print(1)
                    FINAL_RESULT = soup.find("div", {"class": "iKJnec"}).getText()

    soup1 = BeautifulSoup(decodedResponse, "lxml")

    search_suggestion = soup1.find('a',
                                   {"id": 'fprsl'})

    search_suggestion_text = ''
    if search_suggestion is not None:
        search_suggestion_text = 'Did you mean ' + stylish_text(search_suggestion.getText()) + ';'

    FINAL_RESULT = search_suggestion_text + ' ' + FINAL_RESULT

    return [FINAL_RESULT, MATCH_SOURCE_NAME]


def bingScrape(text):
    targetURL = BING_SEARCH_URL + quote(text, safe='')
    web_request = request.Request(targetURL)
    web_request.add_header("User-Agent", USER_AGENT)

    response = request.urlopen(web_request).read()
    decodedResponse = response.decode(DECODING_FORMAT)

    bsSoup = BeautifulSoup(decodedResponse, HTML_PARSE_FORMAT)

    try:
        content = bsSoup.find("div", {"class": "b_lBottom"}).getText()

        return content
    except Exception:
        return "No results found"
