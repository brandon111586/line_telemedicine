from linebot.models import *
import re


#醫聯網視訊診療服務 註冊步驟說明頁
def video_step():
  video_step_message = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://med-net.com/Images/newLogo/%E5%BD%A9%E8%89%B2%E7%84%A1%E6%A8%99%E8%AA%9E.webp",
    "size": "250px",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "http://linecorp.com/"
    },
    "backgroundColor": "#ffffff",
    "margin": "none"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "醫聯網 視訊診療服務",
        "weight": "bold",
        "size": "xl",
        "align": "center",
        "style": "normal",
        "offsetTop": "none",
        "offsetBottom": "none",
        "offsetStart": "none"
      },
      {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "icon",
            "url": "https://cdn-icons-png.flaticon.com/512/7933/7933076.png",
            "offsetEnd": "none",
            "offsetStart": "none",
            "margin": "none",
            "size": "xl",
            "offsetBottom": "none",
            "offsetTop": "xs"
          },
          {
            "type": "text",
            "text": "註冊步驟：",
            "margin": "none",
            "offsetBottom": "none",
            "offsetStart": "sm",
            "size": "md",
            "weight": "regular"
          }
        ],
        "margin": "none",
        "offsetTop": "md",
        "offsetBottom": "none"
      },
      {
        "type": "box",
        "layout": "baseline",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "text",
            "text": "1. 輸入個人基本資料",
            "color": "#666666",
            "size": "md",
            "wrap": True
          }
        ],
        "offsetTop": "none"
      },
      {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "text",
            "text": "2. 將健保卡拍照上傳至對話框",
            "size": "md",
            "color": "#666666"
          }
        ]
      },
      {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "text",
            "text": "3. 點選連結使用視訊服務",
            "color": "#666666",
            "size": "md"
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "primary",
        "height": "sm",
        "action": {
          "type": "postback",
          "label": "開始註冊",
          "data": "@個人資料",
          "displayText": "開始註冊"
        },
        "color": "#0088e1"
      },
      {
        "type": "box",
        "layout": "vertical",
        "contents": [],
        "margin": "sm"
      }
    ],
    "flex": 0
  }
}
  flex_message = FlexSendMessage(
                alt_text='視訊診療服務',
                contents= video_step_message #json貼在這裡
            )
  return flex_message



#Step1-1
Step1_1 = "請輸入您的姓名"
def regex_name(text):
  regex = r"[\u4e00-\u9FEF]{2,4}"
  matches = re.match(regex,text)
  if matches == None:
    result = "fail"
  elif matches[0] ==text:
    result =  matches[0]
  else:
    result = 'fail'
  return result



#Step1-3
def select_gender():
    confirm_template_message = TemplateSendMessage(
             alt_text='性別',
             template=ConfirmTemplate(
                 text='請選擇性別',
                 actions=[
                     PostbackAction(
                         label='男',
                         data='@健保卡:男',
                         text='男'
                     ),
                     PostbackAction(
                         label='女',
                         data='@健保卡:女',
                         text ='女'
                     )
                 ]
             )
         )
    return confirm_template_message


#進入視訊診間

def enter_video():
  enter_video_message = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://miro.medium.com/max/1838/1*To-mV5EPuZyNelPE1fM75g.png",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "http://linecorp.com/"
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "weight": "bold",
        "size": "xl",
        "text": "開始視訊診療服務",
        "align": "center",
        "offsetBottom": "none"
      },
      {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "icon",
            "url": "https://cdn-icons-png.flaticon.com/512/190/190411.png",
            "position": "relative",
            "offsetStart": "none"
          },
          {
            "type": "text",
            "text": "預約已完成",
            "margin": "sm",
            "offsetEnd": "none"
          }
        ],
        "margin": "lg"
      },
      {
        "type": "text",
        "text": "請在預約時間點擊視訊連結\n即可與醫師進行視訊診療",
        "margin": "xs",
        "wrap": True
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "primary",
        "height": "sm",
        "action": {
          "type": "uri",
          "label": "進入視訊診間",
          "uri": "https://aidoctor.med-net.com/onlineExhibition/product"
        },
        "color": "#0088e0"
      }
    ],
    "flex": 0
  }
}
  flex_message = FlexSendMessage(
                alt_text='進入視訊診間',
                contents= enter_video_message #json貼在這裡
            )
  return flex_message




#確認預約時間
def reserve_confirm(date,time):
  reserve_confirm_message = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://i.imgur.com/wmees0t.png",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "http://linecorp.com/"
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "確認預約時間",
        "weight": "bold",
        "size": "xl",
        "align": "center"
      },
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "text",
            "text": "日期",
            "offsetEnd": "none",
            "margin": "none",
            "size": "lg"
          },
          {
            "type": "text",
            "text": date,
            "align": "start",
            "size": "lg"
          }
        ],
        "offsetTop": "md"
      },
      {
        "type": "separator",
        "margin": "xl"
      },
      {
        "type": "box",
        "layout": "baseline",
        "contents": [
          {
            "type": "text",
            "text": "時段",
            "margin": "none",
            "size": "lg"
          },
          {
            "type": "text",
            "text": time,
            "size": "lg"
          }
        ],
        "offsetTop": "md"
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "primary",
        "height": "md",
        "action": {
          "type": "postback",
          "data": "@預約成功",
          "displayText": "預約確認",
          "label": "確認"
        },
        "color": "#0087e0"
      },
        {
        "type": "box",
        "layout": "vertical",
        "contents": []
      }
    ],
    "flex": 0,
    "offsetTop": "md",
    "offsetBottom": "none",
    "margin": "none"
  }
}
  flex_message = FlexSendMessage(
                alt_text='確認預約時間',
                contents= reserve_confirm_message #json貼在這裡
            )
  return flex_message
