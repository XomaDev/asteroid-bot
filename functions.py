import base64
import re


def encode(text):
    return base64.b64encode(text.encode("ASCII")).decode()


def enhanceText(text):
    text = text.replace('.', '.', text.count('.')).replace(',', ', ', text.count(','))
    text = " ".join(text.split()).replace(" . ", ". ")
    return text


def stylish_text(text):
    text = text.lower()
    style_text = list('𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇')
    normal_text = list('abcdefghijklmnopqrstuvwxyz')

    result = []

    for char in list(text):
        if char in normal_text:
            result.append(style_text[normal_text.index(char)])
        else:
            result.append(char)

    return ''.join(result)


def checkForURLs(string):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]
