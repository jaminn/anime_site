import requests, re
import urllib.request
from urllib.parse import quote, unquote
from bs4 import BeautifulSoup
import execjs


def get_anigod_video(past_url):
    url = unquote(past_url)
    print(url)
    patt = r"var videoID = ?'(.*?)';"
    hdr = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive',
        'referer': 'http://t.umblr.com/'}
    videoID = []
    req = urllib.request.Request(url, headers=hdr)
    data = urllib.request.urlopen(req)
    soup = BeautifulSoup(data)
    text = soup.get_text()
    videoID = re.findall(patt, text)
    ID = execjs.eval('encodeURIComponent("' + videoID[0] + '")')
    return 'https://anigod.com/video?id=' + ID
    # return 'https://anigod.com/video?id='+quote(videoID[0],safe='')


if __name__ == "__main__":
    url = "https://anigod.com/episode/%EB%B0%94%EB%82%98%EB%83%90-4%ED%99%94-23940"
    print(get_anigod_video(quote(url,safe='')))
