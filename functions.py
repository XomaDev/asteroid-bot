import base64


def encode(text):
    return base64.b64encode(text.encode("ASCII")).decode()


def enhanceText(text):
    text = text.replace('.', '.', text.count('.')).replace(',', ', ', text.count(','))
    text = " ".join(text.split()).replace(" . ", ". ")
    return text
