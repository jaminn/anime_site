import pymongo
import os
from flask import Flask, render_template, url_for
from urllib import parse
from get_anigod_video import  get_anigod_video

app = Flask(__name__)
#client = pymongo.MongoClient("mongodb://rnnwkals1:hi000319@ds041939.mlab.com:41939/ani_db")
client = pymongo.MongoClient("mongodb://localhost:27017/ani_db")
db = client.ani_db


@app.context_processor
def select():
    def _select(value, i):
        return "selected" if (value-1 % 10)+1 == i else " "
    return dict(select=_select)
#
# @app.context_processor
# def quote():
#     def _quote(uri):
#         return parse.quote(uri, safe='')
#     return dict(quote=_quote)
@app.template_filter(name="quote")
def quote(uri):
    return parse.quote(uri, safe='')


def query2db(query):
    anis = db.anime3.find_one({"info.name": {"$regex": query + ""}})
    #anis = db.anime2.find_one({"info.name": {"$regex": query + ""}})
    # print(anis["info"]["name"])
    # print(anis["info"]["sumnail"])
    # for ani in anis["list"]:
    #     print(ani["name"], ani["url"], ani["sumnail"])
    return anis


@app.route('/')
def hello():
    return "hello world!"

@app.route('/video/<query>')
def video(query):
    return '<video controls><source type="video/mp4" src="%s"></video>' % get_anigod_video(query)


@app.route('/<query>')
def index(query):
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


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
