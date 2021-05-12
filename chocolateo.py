# Requirements:
#
# - URLLIB
# - BeautifulSoup
# - LXML


from urllib import request
from urllib.parse import quote
from info import USER_AGENT, DECODING_FORMAT, HTML_PARSE_FORMAT
from bs4 import BeautifulSoup

SEARCH_URL = "https://www.google.com/search?q="
BING_SEARCH_URL = "https://www.bing.com/search?q="

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
DICTIONARY_MEANING_TAG = "L1jWkf h3TRxf"

# Search results

SEARCH_RESULT_TYPE = "span"
SEARCH_RESULT_TAG = "aCOpRe"
SEARCH_MATCH_TYPE = "cite"
SEARCH_MATCH_TAG = "iUh30 Zu0yb qLRx3b tjvcx"


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

    meanings = soup.find_all(DICTIONARY_MEANING_TYPE,
                             {"class": DICTIONARY_MEANING_TAG})
    meanings_arranged = []

    for meaning in meanings:
        text = meaning.getText()
        text = text[0].upper() + text[1:]
        meanings_arranged.append(text)

    if len(meanings_arranged) > 0:
        for meaning in meanings_arranged:
            FINAL_RESULT = FINAL_RESULT + "-  " + meaning + "\n\n"

    # Search

    if len(FINAL_RESULT) == 0:
        soup = bsSoup
        FINAL_RESULT = soup.find(SEARCH_RESULT_TYPE, {"class": SEARCH_RESULT_TAG}).getText()
        text = soup.find(SEARCH_MATCH_TYPE, {"class": SEARCH_MATCH_TAG}).getText()
        MATCH_SOURCE_NAME = text.replace(" › ", "/")

        newSoup = BeautifulSoup(decodedResponse, "lxml")

        children = newSoup.find("div", {"class": "tF2Cxc"}).findChildren("a")

        if children[0].get("href") != "":
            MATCH_SOURCE_NAME = (children[0].get("href"))

        if FINAL_RESULT == "":
            try:
                FINAL_RESULT = soup.find("div", {"class": "RqBzHd"}).getText()
            except:
                try:
                    FINAL_RESULT = soup.find("span", {"class": "hgKElc"}).getText()
                except:
                    FINAL_RESULT = soup.find("div", {"class": "iKJnec"}).getText()

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
