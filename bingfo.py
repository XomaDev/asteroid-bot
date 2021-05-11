from urllib.parse import quote
from urllib import request
from bs4 import BeautifulSoup

from info import USER_AGENT, DECODING_FORMAT, HTML_PARSE_FORMAT

SEARCH_URL = "https://www.bing.com/search?q="


def bingScrape(text):
    targetURL = SEARCH_URL + quote(text, safe='')
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
