from numbers import Real
from flask import Flask
from datetime import datetime,date
import pymongo,json
from bson.json_util import dumps   #bson轉json 轉json 
import json
from flask_cors import CORS
from flask import jsonify
import random
# app = Flask(__name__)
# CORS(app)
client = pymongo.MongoClient("mongodb+srv://brandon:65432122010@linebot.xjvgoas.mongodb.net/?retryWrites=true&w=majority")
db = client.user
collection =db.user_data

# @app.route("/mongoapi")
# def hello_world():
#     today = date.today()
#     today = str(today)
#     # result = list(collection.find({"Reserve_Date":today}))
#     result = list(collection.find())
#     json_data = dumps(result) #先將list轉成bson
#     json_data = json.loads(json_data)  #bson轉Json
#     # json_data = str(json_data)
    
#     return jsonify(json_data)

# #主程式
# import os
# if __name__ == "__main__":
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='127.0.0.1', port=port, debug=True)
# result = list(collection.find())
# json_data = json.loads(dumps(result))
# print(json_data)


# for  column in datatable_column:
#     print(json_data[0][column])
# print(json_data)

# reserve_data = {'data':json_data} #整理成jquery table吃的json格式
import uuid
def getUUID():
    return "".join(str(uuid.uuid4()).split("-")).upper()
telemedicine_number = getUUID()
x = "https://stage.med-net.com/mednetVideo/index_m_d.html#"+telemedicine_number
print(x)
