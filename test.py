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
from operator import itemgetter
app = Flask(__name__)
CORS(app)
client = pymongo.MongoClient("mongodb+srv://brandon:65432122010@linebot.xjvgoas.mongodb.net/?retryWrites=true&w=majority")
db = client.user
collection =db.user_data

@app.route('/report_export') #匯出報表功能分頁需要的Data 
def make_report():
    result = list(collection.find({"Reserve_Date":{"$ne":""}})) #只回傳有預約的病患名單
    
    data_list = [] #用來儲存整理後的名單
    for i in result:
        data = {
            "姓名":i['Real_name'],
            "暱稱":i['Line_name'],
            "年齡":i['Age'],
            '性別':i['Gender'],
            '預約日期':i['Reserve_Date'],
            '預約時間':i['Reserve_Time']
            }
        data_list.append(data)
    data_list = sorted(data_list,key=itemgetter('預約日期')) #按照預約日期進行排序
    
    return jsonify(data_list)


#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=True)