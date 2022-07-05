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
from register import *
import pymongo


app = Flask(__name__)



# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('rTIVtyQMX7seAHTiLsgZZlBKT1qhMw73M0FKKRqHzXgoIsJqy6gKaCTlEVhW6ypYZadFGKmToZkST07VR4BeYs7cpTE2uyKoYa2lvJ1M3t0lZShblDxYriXgVA0G4erj6RifbV1FRYzsWCT+6Vh9eAdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('bd2b796ce8eba9b6114cf1daaca1437b')

status = ""




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
    global status #紀錄狀態

   
    msg_type = event.message.type
    if msg_type == 'text':
        msg = event.message.text
    else :
        msg = 'image'
    profile = line_bot_api.get_profile(event.source.user_id)
    user_name = profile.display_name
    user_id = profile.user_id

#開啟視訊診療服務說明頁
    if (msg =="視訊"):
        line_bot_api.reply_message(event.reply_token,video_step())
#1-1 檢驗姓名(規則:2-4個中文字)
    if status =='1-1':
        print(1-1)
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

                line_bot_api.reply_message(event.reply_token,[TextSendMessage(welcome_message,emojis=emoji),TextSendMessage('請輸入您的年齡')])
                status='1-2'
        
#1-2 檢驗年齡(規則：5~130歲)
    if status =='1-2':
        print('1-2')
        name_range = []
        for i in range(5,130):
            name_range.append(str(i))
        if msg in name_range:
            status ='1-3'
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
    if status == '2-1':
        if (msg_type == 'image'):
            emoji = [
                            {
                                "index": 5,
                                "productId": "5ac2216f040ab15980c9b448",
                                "emojiId": "001"
                            }
                        ]
            line_bot_api.reply_message(event.reply_token,[TextSendMessage(text='已收到圖片$，感謝您的配合!',emojis=emoji),enter_video()])
            
            message_content = line_bot_api.get_message_content(event.message.id)
            image_name = user_id +"_"+ user_name + "_健保卡資訊"
            path = './Image/'+image_name+'.png'
            with open(path, 'wb') as fd:
                for chunk in message_content.iter_content():
                    fd.write(chunk)
            status = ""

    
        

    
@handler.add(PostbackEvent)
def handle_postback(event):
    global status
    post_msg = event.postback.data
    
    profile = line_bot_api.get_profile(event.source.user_id)
    user_name = profile.display_name
    user_id = profile.user_id

#1-1 點擊開始註冊後 詢問姓名
    if post_msg == "@個人資料":
        
        line_bot_api.reply_message(event.reply_token,TextSendMessage("請輸入您的姓名"))
        status='1-1'
    
    # return 0


#2-1 輸入健保卡照片
    if post_msg == "@健保卡":
        status = "2-1"
        line_bot_api.reply_message(event.reply_token,TextSendMessage("請將健保卡拍照後上傳至對話框"))



#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=True)