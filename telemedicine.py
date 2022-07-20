from typing import Text
from unicodedata import name
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler,WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re 
from flex_message import *
from controll_mongodb import update_data, update_status  #更新mongoDB資料
import pymongo,json
from datetime import datetime,date  #抓今日時間
from flask_cors import CORS
import uuid  #視訊連結使用
import gridfs  #存健保卡圖片到mongoDB

app = Flask(__name__)
CORS(app)
# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('rTIVtyQMX7seAHTiLsgZZlBKT1qhMw73M0FKKRqHzXgoIsJqy6gKaCTlEVhW6ypYZadFGKmToZkST07VR4BeYs7cpTE2uyKoYa2lvJ1M3t0lZShblDxYriXgVA0G4erj6RifbV1FRYzsWCT+6Vh9eAdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('bd2b796ce8eba9b6114cf1daaca1437b')

#mongodb連線
client = pymongo.MongoClient("mongodb+srv://brandon:65432122010@linebot.xjvgoas.mongodb.net/?retryWrites=true&w=majority")
db = client.user
collection =db.user_data
# order_list = db.order_list


# ==============使用者資料格式===============
# user_data = {
#             "Line_id":user_id,
#             "Line_name":user_name,
#             "Real_name":"",
#             "Age":"",
#             "Gender":"",
#             "Status":""
#             "Reserve_Time":""
#             }

@app.route("/callback", methods=['POST'])
def callback():
# get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    
    # get request body as text
    body = request.get_data(as_text=True)
   
    
    app.logger.info("Request body: " + body)
    
    
    
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'



@handler.add(MessageEvent, message=(TextMessage,ImageMessage))
def handle_message(event):

#判斷用戶輸入的是哪種資料(文字or圖片)
    msg_type = event.message.type 
    if msg_type == 'text':
        msg = event.message.text
    else :
        msg = 'image'

#取得Line用戶資料
    profile = line_bot_api.get_profile(event.source.user_id)
    user_name = profile.display_name
    user_id = profile.user_id
    
    #取得使用者目前資料庫裡的資料
    x = collection.find_one({"Line_id":user_id})
    if x == None:
        #建立user在mongodb的資料表(存個人基本資料 & 判斷目前流程的Status)
        user_data = {
            "Line_id":user_id,
            "Line_name":user_name,
            "Real_name":"",
            "Age":"",
            "Gender":"",
            "Status":"",
            "Reserve_Date":"",
            "Reserve_Time":"",
            "Video_link":"",
            "Health_card_image":""
            }
        #若使用者尚未建立資料就幫他建立一份
        x = collection.insert_one(user_data)
        

#****************************視訊診療註冊流程*********************************
#開啟視訊診療服務說明頁
    if (msg =="註冊"):
        x = collection.find_one({"Line_id":user_id})
        #如果狀態為"已註冊"就直接給使用者視訊連結
        if x['Status'] =='已註冊':
            line_bot_api.reply_message(event.reply_token,TextSendMessage("您已註冊完成!"))
        line_bot_api.reply_message(event.reply_token,video_step())
#1-1 檢驗姓名(規則:2-4個中文字)
    if x['Status'] =='1-1':
        if msg_type == "text":
            name_ok =regex_name(msg)
            
            #如果輸入的姓名不符規則
            if name_ok=='fail':
                emoji = [
                            {
                                "index": 4,
                                "productId": "5ac21a18040ab15980c9b43e",
                                "emojiId": "005"
                            }
                        ]
                line_bot_api.reply_message(event.reply_token,[TextSendMessage(text='輸入錯誤$',emojis=emoji),TextSendMessage('請輸入正確的姓名')])

            #如果符合規則    
            else:
                welcome_message = msg+"您好!\n歡迎使用視訊診療服務$"
                emoji_index = len(welcome_message)-1
                emoji = [
                            {
                                "index": emoji_index,
                                "productId": "5ac1bfd5040ab15980c9b435",
                                "emojiId": "009"
                            }
                        ]
                update_data(user_id,"Real_name",msg,collection)
                line_bot_api.reply_message(event.reply_token,[TextSendMessage(welcome_message,emojis=emoji),TextSendMessage('請輸入您的年齡')])
                update_status(user_id,"1-2",collection)
        
#1-2 檢驗年齡(規則：5~130歲)
    if x['Status'] =='1-2':
        name_range = []
        for i in range(5,130):
            name_range.append(str(i))
        if msg in name_range:
            update_status(user_id,"1-3",collection) #更新狀態
            update_data(user_id,"Age",msg,collection) #紀錄年齡
            line_bot_api.reply_message(event.reply_token,select_gender())
        else:
            emoji = [
                            {
                                "index": 4,
                                "productId": "5ac21a18040ab15980c9b43e",
                                "emojiId": "005"
                            }
                        ]
            
            line_bot_api.reply_message(event.reply_token,[TextSendMessage(text='輸入錯誤$',emojis=emoji),TextSendMessage('請輸入正確的年齡')])
            


            
    
#2-1 健保卡上傳到對話框
    if x['Status'] == '2-1':
        if (msg_type == 'image'):
            emoji = [
                            {
                                "index": 5,
                                "productId": "5ac2216f040ab15980c9b448",
                                "emojiId": "001"
                            }
                        ]
            want_reserve=QuickReply(items=[
                QuickReplyButton(action=PostbackAction(label="門診預約",data="@預約",text="門診預約")),
                ])
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='已收到圖片$，感謝您的配合!',emojis=emoji,quick_reply=want_reserve))
            
            message_content = line_bot_api.get_message_content(event.message.id)
            image_name = user_id +"_"+ user_name + "_健保卡資訊"
            path = './Image/'+image_name+'.png'
            with open(path, 'wb') as fd:
                for chunk in message_content.iter_content():
                    fd.write(chunk)
            with open(path,'rb') as f:
                print(path)
                contents = f.read()
                
                update_data(user_id,"Health_card_image",contents,collection)   
            
            update_status(user_id,"已註冊",collection)
        if (msg_type!="image" and msg!="男" and msg!="女"):
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='請上傳健保卡圖片到對話框'))
 #****************************視訊診療註冊流程*********************************   


 #*********************************預約看診時間**********************************
    if (msg == "預約"):
        if x['Status']=="已註冊":
            search_time=QuickReply(items=[
                QuickReplyButton(action=PostbackAction(label="星期一",text="星期一",data="@星期一")),
                QuickReplyButton(action=PostbackAction(label="星期二",text="星期二",data="@星期二")),
                QuickReplyButton(action=PostbackAction(label="星期三",text="星期三",data="@星期三")),
                QuickReplyButton(action=PostbackAction(label="星期四",text="星期四",data="@星期四")),
                QuickReplyButton(action=PostbackAction(label="星期五",text="星期五",data="@星期五")),
                ])
            
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="查詢開診時段",quick_reply=search_time))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="請先註冊才能使用預約功能"))

    if (msg[:2]=="星期"):
        day_number=msg[-1]
        choose_time=QuickReply(items=[QuickReplyButton(action=DatetimePickerAction(label="選擇預約時間",data="@選擇日期",mode='datetime')),QuickReplyButton(action=PostbackAction(label="查詢其他時段",text="查詢其他時段",data='@預約'))])
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = "星期"+day_number +"開診時間為:\n上午 10:00 ~ 10:30\n下午 15:00 ~ 15:30",quick_reply=choose_time))
        # if(msg[-1])=="一":
        #     choose_time=QuickReply(items=[QuickReplyButton(action=DatetimePickerAction(label="時間選擇",data="時間選擇",mode='datetime')),
        #     QuickReplyButton(action=PostbackAction(label="查詢其他時段",text="預約",data='預約'))])
        #     line_bot_api.reply_message(event.reply_token,TextSendMessage(text = "星期一 \n上午 10:00 ~ 10:30\n下午 15:00 ~ 15:30",quick_reply=choose_time))
        # if(msg[-1])=="二":
        #     choose_time=QuickReply(items=[QuickReplyButton(action=DatetimePickerAction(label="時間選擇",data="時間選擇",mode='datetime')),
        #     QuickReplyButton(action=PostbackAction(label="查詢其他時段",text="預約",data='預約'))])
        #     line_bot_api.reply_message(event.reply_token,TextSendMessage(text = "星期二 \n上午 10:00 ~ 10:30\n下午 15:00 ~ 15:30",quick_reply=choose_time))
        # if(msg[-1])=="三":
        #     choose_time=QuickReply(items=[QuickReplyButton(action=DatetimePickerAction(label="時間選擇",data="時間選擇",mode='datetime')),
        #     QuickReplyButton(action=PostbackAction(label="查詢其他時段",text="預約",data='預約'))])
        #     line_bot_api.reply_message(event.reply_token,TextSendMessage(text = "星期三 \n上午 10:00 ~ 10:30\n下午 15:00 ~ 15:30",quick_reply=choose_time))
        # if(msg[-1])=="四":
        #     choose_time=QuickReply(items=[QuickReplyButton(action=DatetimePickerAction(label="時間選擇",data="時間選擇",mode='datetime')),
        #     QuickReplyButton(action=PostbackAction(label="查詢其他時段",text="預約",data='預約'))])
        #     line_bot_api.reply_message(event.reply_token,TextSendMessage(text = "星期四 \n上午 10:00 ~ 10:30\n下午 15:00 ~ 15:30",quick_reply=choose_time))
        # if(msg[-1])=="五":
        #     choose_time=QuickReply(items=[QuickReplyButton(action=DatetimePickerAction(label="時間選擇",data="時間選擇",mode='datetime')),
        #     QuickReplyButton(action=PostbackAction(label="查詢其他時段",text="預約",data='預約'))])
        #     line_bot_api.reply_message(event.reply_token,TextSendMessage(text = "星期五 \n上午 10:00 ~ 10:30\n下午 15:00 ~ 15:30",quick_reply=choose_time))
 
 
#**********************************預約看診時間****************************************


#***************************(醫師端)查看今日診單*******************************

   
        


    
@handler.add(PostbackEvent)
def handle_postback(event):
    
    post_msg = event.postback.data
    
    profile = line_bot_api.get_profile(event.source.user_id)
    user_name = profile.display_name
    user_id = profile.user_id

#****************************視訊診療註冊流程*********************************
#點擊醫聯網視訊診療的開始註冊按鈕後 詢問姓名(1-1)
    if post_msg == "@個人資料":
        #如果是第一次註冊就開始進行基本資料問答流程
        line_bot_api.reply_message(event.reply_token,TextSendMessage("請輸入您的姓名\n(請點選左下角對話框輸入)"))
        update_status(user_id,"1-1",collection) #將使用者在資料庫中紀錄的狀態設為1-1
        
        # return 0


#2-1 輸入健保卡照片
    if post_msg[:4] == "@健保卡":
        x = collection.find_one({"Line_id":user_id})
        if x['Status'] =='1-3': #確定他是按照問題順序從1-3來的 不是自己翻對話紀錄回去亂點選項的 
            update_status(user_id,"2-1",collection)
            update_data(user_id,'Gender',post_msg[-1],collection)
            camera_quickreply = QuickReply(items=[
                QuickReplyButton(action=CameraAction(label="開啟相機")),
                QuickReplyButton(action=CameraRollAction(label="打開相簿"))
                ])
            line_bot_api.reply_message(event.reply_token,TextSendMessage("請將健保卡拍照後上傳至對話框",quick_reply=camera_quickreply))
            
#****************************視訊診療註冊流程*********************************




#***************************預約看診時間***************************************
    if (post_msg == "@預約"):
        search_time=QuickReply(items=[
            QuickReplyButton(action=PostbackAction(label="星期一",text="星期一",data="@星期一")),
            QuickReplyButton(action=PostbackAction(label="星期二",text="星期二",data="@星期二")),
            QuickReplyButton(action=PostbackAction(label="星期三",text="星期三",data="@星期三")),
            QuickReplyButton(action=PostbackAction(label="星期四",text="星期四",data="@星期四")),
            QuickReplyButton(action=PostbackAction(label="星期五",text="星期五",data="@星期五")),
            ])
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="查詢開診時段",quick_reply=search_time))

    
    if post_msg == "@選擇日期":
        body = request.get_data(as_text=True)
        #把DatetimePicker選擇後的回應轉JOSN，並拆分成日期&時段
        j = json.loads(body)
        date_data = str(j['events'][0]['postback']['params']['datetime'])
        date_str = date_data[:10]
        time_str = date_data[11:]     
        


        #用日期找出那天是星期幾
        weekday = datetime.strptime(date_str,"%Y-%m-%d") #要把日期轉成datetime格式才能放到isoweekday
        weekday = weekday.isoweekday()    
        num_dict={1:'一',2:"二",3:"三",4:"四",5:"五",6:"六",7:"日"} #iswoweekday回傳值是阿拉伯數字，建字典轉成國字
        weekday = num_dict[weekday]
        
        #如果選到過去的時間，請他重選
        now_date = datetime.now().strftime("%Y-%m-%d")
        now_time = datetime.now().strftime("%H:%M:%S")
        
        if date_str < now_date:
            re_choose_time=QuickReply(items=[QuickReplyButton(action=DatetimePickerAction(label="選擇預約時段",data="@選擇日期",mode='datetime')),
            QuickReplyButton(action=PostbackAction(label="查詢開診時段",text="查詢開診時段",data='@預約'))])
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="您選擇的時段不正確\n請查詢後再輸入時段!",quick_reply=re_choose_time))
        elif date_str == now_date and time_str<now_time:
            re_choose_time=QuickReply(items=[QuickReplyButton(action=DatetimePickerAction(label="選擇預約時段",data="@選擇日期",mode='datetime')),
            QuickReplyButton(action=PostbackAction(label="查詢開診時段",text="查詢開診時段",data='@預約'))])
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="您選擇的時段不正確\n請查詢後再輸入時段!",quick_reply=re_choose_time))

        #如果選擇的時間是有開診的，回傳確認預約時間的flex message
        reserve_list=["一","二","三","四","五"] #假設只有1~5有開診
        if weekday in reserve_list:
            if time_str >= "10:00" and time_str <= "10:30":
                line_bot_api.reply_message(event.reply_token,reserve_confirm(date_str,time_str))
                update_data(user_id,"Reserve_Date",date_str,collection) 
                update_data(user_id,"Reserve_Time",time_str,collection) 
            elif time_str >= "15:00" and time_str <="15:30":
                line_bot_api.reply_message(event.reply_token,reserve_confirm(date_str,time_str))
                update_data(user_id,"Reserve_Date",date_str,collection) 
                update_data(user_id,"Reserve_Time",time_str,collection) 
            else: #如果日期不在開診時段內就請使用者再次選擇日期
                re_choose_time=QuickReply(items=[QuickReplyButton(action=DatetimePickerAction(label="選擇預約時段",data="@選擇日期",mode='datetime')),
                QuickReplyButton(action=PostbackAction(label="查詢開診時段",text="查詢開診時段",data='@預約'))])
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="您選擇的時段沒有開診\n請查詢後再輸入時段!",quick_reply=re_choose_time))
        else: #如果日期不在開診時段內就請使用者再次選擇日期
            re_choose_time=QuickReply(items=[QuickReplyButton(action=DatetimePickerAction(label="選擇預約時段",data="@選擇日期",mode='datetime')),
            QuickReplyButton(action=PostbackAction(label="查詢開診時段",text="查詢開診時段",data='@預約'))])
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="您選擇的時段沒有開診\n請查詢後再輸入時段!",quick_reply=re_choose_time)) 


    if post_msg == "@預約成功":
        def getUUID():
            return "".join(str(uuid.uuid4()).split("-")).upper()
        video_link_uuid = getUUID()
        video_link= "https://stage.med-net.com/mednetVideo/index_m_d.html#"+video_link_uuid
        update_data(user_id,"Video_link",video_link,collection)
        line_bot_api.reply_message(event.reply_token,[TextSendMessage(text="預約成功!"),enter_video(video_link)])
        x = collection.find_one({"Line_id":user_id})
        line_bot_api.push_message("Udebc7a5c95167ff61b2872004187ab16", get_new_reserve(x["Real_name"],x['Line_name'],x['Gender'],x["Age"],x["Reserve_Date"],x['Reserve_Time'],x['Video_link']))
#**************************************預約看診時間******************************************
from bson.json_util import dumps   #bson轉json 轉json 
@app.route("/mongoapi")
def hello_world():
    # today = date.today()
    # today = str(today)
    # result = list(collection.find({"Reserve_Date":today}))

    # return "今日診單"+result
    result = list(collection.find({"Reserve_Date":{"$ne":""}})) #只回傳有預約的病患名單
    json_data = json.loads(dumps(result))
    reserve_data = {'data':json_data} #整理成jquery table吃的json格式   
    return reserve_data

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=True)