from numbers import Real
from flask import Flask
from datetime import datetime,date
import pymongo,json
from bson.json_util import dumps   #bson轉json 轉json 
import json
from flask_cors import CORS
from flask import jsonify
import random
from controll_mongodb import *
from bson.json_util import dumps
app = Flask(__name__)
CORS(app)
client = pymongo.MongoClient("mongodb+srv://brandon:65432122010@linebot.xjvgoas.mongodb.net/?retryWrites=true&w=majority")
db = client.user
collection =db.user_data

file = r"Image\U9dea29ad751a3faac2a17761eee5dd5a_廖建凱_健保卡資訊.png"
with open(file,'rb') as f:
    contents = f.read()
update_data("Udebc7a5c95167ff61b2872004187ab16","Health_card_image",contents,collection)
import base64
@app.route("/mongoapi")
def hello_world():
    # today = date.today()
    # today = str(today)
    # result = list(collection.find({"Reserve_Date":today}))
    # result = list(collection.find())
    # json_data = dumps(result) #先將list轉成bson
    # json_data = json.loads(json_data)  #bson轉Json
    # json_data = str(json_data)
    result = list(collection.find({"Reserve_Date":{"$ne":""}}))
    json_data = json.loads(dumps(result))
    reserve_data = {'data':json_data} #整理成jquery table吃的json格式   
    # print(json_data[3]["Health_card_image"])
    for i in reserve_data['data']:
        print(i['Real_name'])
    return reserve_data
    

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=True)
# result = list(collection.find())
# json_data = json.loads(dumps(result))
# print(json_data)


# for  column in datatable_column:
#     print(json_data[0][column])
# print(json_data)

# reserve_data = {'data':json_data} #整理成jquery table吃的json格式
# import uuid
# def getUUID():
#     return "".join(str(uuid.uuid4()).split("-")).upper()
# telemedicine_number = getUUID()
# x = "https://stage.med-net.com/mednetVideo/index_m_d.html#"+telemedicine_number
# print(x)
