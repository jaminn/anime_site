import requests, re
from urllib.parse import quote, unquote
import execjs


def get_anigod_video(past_url):
    url = unquote(past_url)
    headers = {'referer': 'http://t.umblr.com/'}
    text = requests.get(url, headers=headers).text
    while not text:
        text = requests.get(url, headers=headers).text
    patt = r"var videoID = ?'(.*?)';"
    videoID = re.findall(patt, text)
    ID = execjs.eval('encodeURIComponent("' + videoID[0] + '")')
    return 'https://anigod.com/video?id=' + ID
    # return 'https://anigod.com/video?id='+quote(videoID[0],safe='')


if __name__ == "__main__":
    url = "https://anigod.com/episode/%ea%b0%95%ec%b2%a0-%ec%98%a4%ec%bc%80%ec%8a%a4%ed%8a%b8%eb%9d%bc-2%ed%99%94-29549"
    print(get_anigod_video(url))
