import pymongo
from flask import Flask, render_template

app = Flask(__name__)
client = pymongo.MongoClient("mongodb://rnnwkals1:hi000319@ds041939.mlab.com:41939/ani_db")
db = client.ani_db
print(db.anime2.find_one({"info.name": {"$regex": "나"}}))
def query2db(query):
    anis = db.anime2.find_one({"info.name": {"$regex": query+""}})
    # print(anis["info"]["name"])
    # print(anis["info"]["sumnail"])
    # for ani in anis["list"]:
    #     print(ani["name"], ani["url"], ani["sumnail"])
    return anis

#
# @app.route('/<query>')
# def index(query):
#     anis = query2db(query)
#     return render_template("ani_page.html", anis=anis)
#
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
