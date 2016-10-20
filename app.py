import pymongo
import os
from flask import Flask, render_template, url_for, redirect
from urllib import parse

from flask import request
import requests

from get_anigod_video import get_anigod_video
from flask_cors import CORS, cross_origin

app = Flask(__name__)
client = pymongo.MongoClient("mongodb://rnnwkals1:hi000319@ds041939.mlab.com:41939/ani_db")
# client = pymongo.MongoClient("mongodb://localhost:27017/ani_db")
db = client.ani_db
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.context_processor
def select():
    def _select(value, i):
        return "selected" if (value - 1 % 10) + 1 == i else " "

    return dict(select=_select)


@app.template_filter(name="quote")
def quote(uri):
    return parse.quote(uri, safe='')


def query2db(query):
    anis = db.anime3.find_one({"info.name": {"$regex": query + ""}})
    # anis = db.anime2.find_one({"info.name": {"$regex": query + ""}})
    # print(anis["info"]["name"])
    # print(anis["info"]["sumnail"])
    # for ani in anis["list"]:
    #     print(ani["name"], ani["url"], ani["sumnail"])
    return anis


@app.route('/')
def index():
    return "hello world!"


@app.route('/video', methods=['POST', 'GET'])
def video():
    if request.method == 'GET':
        return redirect(url_for('video_num', query=request.args.get('input')))
    return redirect(url_for('index'))


@app.route('/video/<query>')
def video_num(query):
    # return '<video controls><source type="video/mp4" src="%s"></video>' % get_anigod_video(query)
    return redirect(get_anigod_video(query))


@app.route('/<query>')
def ani_name(query):
    anis = query2db(query)
    if anis:
        return render_template("ani_page.html", query=query, anis=anis, num=1)
    else:
        return "404"


@app.route('/<query>/<int:num>')
def move_page(query, num):
    anis = query2db(query)
    if anis:
        return render_template("ani_page.html", query=query, anis=anis, num=num)
    else:
        return "404"


@app.route('/test')
def test():
    url = 'https://anigod.com/episode/%EC%95%BC%EB%A7%88%EB%85%B8%EC%8A%A4%EC%8A%A4%EB%A9%94-2%EA%B8%B0-OVA-1%ED%99%94-29334'
    headers = {
        "Host": "anigod.com",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36",
        'referer': 'http://t.umblr.com/'
    }
    req = requests.get(url, headers=headers)
    return str(req.request) + " :" + str(req.text)


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
