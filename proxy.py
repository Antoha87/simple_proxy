from flask import Flask, request
from requests import get
from bs4 import BeautifulSoup
import re


app = Flask(__name__)

SITE_NAME = 'https://habr.com'
HOST = '0.0.0.0'
PORT = 8080


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    result = get(f'{SITE_NAME}{request.full_path}')
    content = result.content.decode(encoding='utf-8', errors='ignore')
    content_with_local_urls = re.sub(r"{}".format(SITE_NAME), f{HOST:PORT}, content)	
    soup = BeautifulSoup(content_with_local_urls, 'html.parser')
    body = soup.find('body')
    process(body)
    return str.encode(str(soup))

def add_tm_string(string):
    return re.sub(r'(\b([a-zA-Zа-яА-Я]{6})\b)', r'\1™', string)

def process(body):
    if hasattr(body, 'contents'):
        for index, fragment in enumerate(body.contents):
            if str(type(fragment)) == "<class 'bs4.element.NavigableString'>":
                text = add_tm_string(str(fragment))
                body.contents[index].replaceWith(text)
            else:
                process(fragment)


if __name__ == '__main__':
  app.run(host=HOST, port=PORT)
