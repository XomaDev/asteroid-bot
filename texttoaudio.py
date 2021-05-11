from urllib import request
from urllib.parse import quote

from info import USER_AGENT


def toAudio(text):
    targetURL = "https://translate.google.com.vn/translate_tts?ie=UTF-8&q=" + quote(text,
                                                                                    safe='') + "&tl=en&client=tw-ob"
    web_request = request.Request(targetURL)
    web_request.add_header("User-Agent", USER_AGENT)

    response = request.urlopen(web_request).read()
    return response
