import requests, re
import urllib.request
from urllib.parse import quote, unquote
from bs4 import BeautifulSoup
import execjs
from flask import g



def get_anigod_video(past_url):
    url = unquote(past_url)
    print(url)
    return url


if __name__ == "__main__":
    url = "https://anigod.com/episode/%EB%B0%94%EB%82%98%EB%83%90-4%ED%99%94-23940"
    print(get_anigod_video(quote(url, safe='')))
