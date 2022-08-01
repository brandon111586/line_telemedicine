from cgi import test
from time import time
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

def enter_video(video_link):
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
          "uri":video_link,
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





#收到新的診單(醫師端)
def get_new_reserve(real_name,line_name,gender,age,date_data,time_data,video_link):
  get_new_reserve_message = {
  "type": "bubble",
  "size": "mega",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "新的診單",
        "weight": "bold",
        "color": "#1DB446",
        "size": "md"
      },
      {
        "type": "text",
        "text": real_name,
        "weight": "bold",
        "size": "xxl",
        "margin": "md"
      },
      {
        "type": "separator",
        "margin": "xl"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "xl",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "Line 暱稱",
                "size": "lg",
                "flex": 0,
                "color": "#555555"
              },
              {
                "type": "text",
                "text": line_name,
                "size": "lg",
                "align": "end"
              }
            ]
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "性別",
                "size": "lg",
                "color": "#555555",
                "flex": 0
              },
              {
                "type": "text",
                "text": gender,
                "size": "lg",
                "color": "#111111",
                "align": "end"
              }
            ]
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "年齡",
                "size": "lg",
                "color": "#555555",
                "flex": 0
              },
              {
                "type": "text",
                "text": age,
                "size": "lg",
                "color": "#111111",
                "align": "end"
              }
            ]
          },
          {
            "type": "separator",
            "margin": "xl"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "預約日期",
                "flex": 0,
                "size": "lg"
              },
              {
                "type": "text",
                "text": date_data,
                "align": "end",
                "size": "lg"
              }
            ],
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "預約時間",
                "flex": 0,
                "size": "lg"
              },
              {
                "type": "text",
                "text": time_data,
                "size": "lg",
                "align": "end"
              }
            ]
          }
        ]
      },
      {
        "type": "separator",
        "margin": "xxl"
      },
      {
        "type": "box",
        "layout": "horizontal",
        "margin": "lg",
        "contents": [
          {
            "type": "button",
            "action": {
              "type": "uri",
              "label": "進入視訊診間",
              "uri": video_link
            },
            "style": "primary",
            "margin": "none",
            "height": "md"
          }
        ]
      }
    ]
  },
  "styles": {
    "footer": {
      "separator": True
    }
  }
}
  flex_message = FlexSendMessage(
                alt_text='確認預約時間',
                contents= get_new_reserve_message #json貼在這裡
            )
  return flex_message


def clinic_opentime(clinic_date,clinic_time):
  
  def time_open_or_not(date,time): #利用前端送來的資料，判斷該時段是否有開診，有開診回傳打勾勾圖案，沒開診就回傳空白圖案
    if time in clinic_date[date]:
      return "https://cdn-icons-png.flaticon.com/512/1828/1828643.png"
    else:
      return "https://imgur.com/gallery/IcXZRON"

  get_clinic_opentime={
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "門診時間表",
                "size": "3xl",
                "weight": "bold",
                "align": "center",
                "color": "#6c757d"
              }
            ]
          }
        ],
        "margin": "none"
      },
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "borderColor": "#6c757d",
                "borderWidth": "normal",
                "margin": "none",
                "width": "50px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "一",
                    "size": "lg",
                    "color": "#6c757d",
                    "weight": "bold",
                    "align": "center"
                  }
                ],
                "borderColor": "#6c757d",
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "二",
                    "size": "lg",
                    "color": "#6c757d",
                    "weight": "bold",
                    "align": "center"
                  }
                ],
                "borderColor": "#6c757d",
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "三",
                    "size": "lg",
                    "color": "#6c757d",
                    "weight": "bold",
                    "align": "center"
                  }
                ],
                "borderColor": "#6c757d",
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "四",
                    "size": "lg",
                    "color": "#6c757d",
                    "weight": "bold",
                    "align": "center"
                  }
                ],
                "borderColor": "#6c757d",
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "五",
                    "size": "lg",
                    "color": "#6c757d",
                    "weight": "bold",
                    "align": "center"
                  }
                ],
                "borderColor": "#6c757d",
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "六",
                    "size": "lg",
                    "color": "#6c757d",
                    "weight": "bold",
                    "align": "center"
                  }
                ],
                "borderColor": "#6c757d",
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "日",
                    "size": "lg",
                    "color": "#6c757d",
                    "weight": "bold",
                    "align": "center"
                  }
                ],
                "borderColor": "#6c757d",
                "borderWidth": "light"
              }
            ],
            "height": "30px",
            "borderWidth": "normal",
            "borderColor": "#6c757d"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "早上",
                    "size": "xl",
                    "color": "#6c757d",
                    "align": "center",
                    "weight": "bold",
                    "margin": "sm"
                  }
                ],
                "borderColor": "#6c757d",
                "borderWidth": "normal",
                "margin": "none",
                "width": "50px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "image",
                    "url": time_open_or_not("星期一","早上"),
                    "margin": "sm"
                  }
                ],
                "borderColor": "#6c757d",
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "image",
                    "url": time_open_or_not("星期二","早上"),
                    "margin": "sm"
                  }
                ],
                "borderColor": "#6c757d",
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "image",
                    "size": "xxs",
                    "offsetTop": "none",
                    "margin": "sm",
                    "url": time_open_or_not("星期三","早上")
                  }
                ],
                "borderColor": "#6c757d",
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "image",
                    "size": "xxs",
                    "offsetTop": "none",
                    "margin": "sm",
                    "url": time_open_or_not("星期四","早上")
                  }
                ],
                "borderColor": "#6c757d",
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "image",
                    "size": "xxs",
                    "offsetTop": "none",
                    "margin": "sm",
                    "url": time_open_or_not("星期五","早上")
                  }
                ],
                "borderColor": "#6c757d",
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "image",
                    "size": "xxs",
                    "offsetTop": "none",
                    "margin": "sm",
                    "url": time_open_or_not("星期六","早上")
                  }
                ],
                "borderColor": "#6c757d",
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "image",
                    "size": "xxs",
                    "offsetTop": "none",
                    "margin": "sm",
                    "url": time_open_or_not("星期日","早上")
                  }
                ],
                "borderColor": "#6c757d",
                "borderWidth": "normal"
              }
            ],
            "height": "40px",
            "borderWidth": "normal",
            "borderColor": "#6c757d"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "下午",
                    "size": "xl",
                    "color": "#6c757d",
                    "weight": "bold",
                    "align": "center",
                    "margin": "sm"
                  }
                ],
                "borderColor": "#6c757d",
                "borderWidth": "normal",
                "margin": "none",
                "width": "50px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "image",
                    "size": "xxs",
                    "offsetTop": "none",
                    "margin": "sm",
                    "url": time_open_or_not("星期一","下午")
                  }
                ],
                "borderColor": "#6c757d",
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "image",
                    "size": "xxs",
                    "offsetTop": "none",
                    "margin": "sm",
                    "url": time_open_or_not("星期二","下午")
                  }
                ],
                "borderColor": "#6c757d",
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "image",
                    "size": "xxs",
                    "offsetTop": "none",
                    "margin": "sm",
                    "url": time_open_or_not("星期三","下午")
                  }
                ],
                "borderColor": "#6c757d",
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "image",
                    "size": "xxs",
                    "offsetTop": "none",
                    "margin": "sm",
                    "url": time_open_or_not("星期四","下午")
                  }
                ],
                "borderColor": "#6c757d",
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "image",
                    "size": "xxs",
                    "offsetTop": "none",
                    "margin": "sm",
                    "url": time_open_or_not("星期五","下午")
                  }
                ],
                "borderColor": "#6c757d",
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "image",
                    "size": "xxs",
                    "offsetTop": "none",
                    "margin": "sm",
                    "url": time_open_or_not("星期六","下午")
                  }
                ],
                "borderColor": "#6c757d",
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "image",
                    "size": "xxs",
                    "offsetTop": "none",
                    "margin": "sm",
                    "url": time_open_or_not("星期日","下午")
                  }
                ],
                "borderColor": "#6c757d",
                "borderWidth": "light"
              }
            ],
            "height": "40px",
            "borderWidth": "normal",
            "borderColor": "#6c757d"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "晚上",
                    "size": "xl",
                    "color": "#6c757d",
                    "weight": "bold",
                    "align": "center",
                    "margin": "sm"
                  }
                ],
                "borderColor": "#6c757d",
                "borderWidth": "normal",
                "margin": "none",
                "width": "50px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "image",
                    "size": "xxs",
                    "offsetTop": "none",
                    "margin": "sm",
                    "url": time_open_or_not("星期一","晚上")
                  }
                ],
                "borderColor": "#6c757d",
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "image",
                    "size": "xxs",
                    "offsetTop": "none",
                    "margin": "sm",
                    "url": time_open_or_not("星期二","晚上")
                  }
                ],
                "borderColor": "#6c757d",
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "image",
                    "size": "xxs",
                    "offsetTop": "none",
                    "margin": "sm",
                    "url": time_open_or_not("星期三","晚上")
                  }
                ],
                "borderColor": "#6c757d",
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "image",
                    "size": "xxs",
                    "offsetTop": "none",
                    "margin": "sm",
                    "url": time_open_or_not("星期四","晚上")
                  }
                ],
                "borderColor": "#6c757d",
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "image",
                    "size": "xxs",
                    "offsetTop": "none",
                    "margin": "sm",
                    "url": time_open_or_not("星期五","晚上")
                  }
                ],
                "borderColor": "#6c757d",
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "image",
                    "size": "xxs",
                    "offsetTop": "none",
                    "margin": "sm",
                    "url": time_open_or_not("星期六","晚上")
                  }
                ],
                "borderColor": "#6c757d",
                "borderWidth": "normal"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "image",
                    "size": "xxs",
                    "offsetTop": "none",
                    "margin": "sm",
                    "url": time_open_or_not("星期日","晚上")
                  }
                ],
                "borderColor": "#6c757d",
                "borderWidth": "light"
              }
            ],
            "height": "40px",
            "borderWidth": "normal",
            "borderColor": "#6c757d"
          }
        ],
        "borderWidth": "normal",
        "borderColor": "#6c757d",
        "width": "260px",
        "margin": "md"
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "早上時段:  "+str(clinic_time[0][0])+" ~ "+str(clinic_time[0][1]),
            "color": "#6c757d",
            "margin": "none",
            "size": "lg",
            "weight": "bold",
            "style": "normal"
          }
        ]
      },
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "下午時段:  "+str(clinic_time[1][0])+" ~ "+str(clinic_time[1][1]),
            "color": "#6c757d",
            "margin": "none",
            "size": "lg",
            "weight": "bold"
          }
        ],
        "margin": "md"
      },
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "晚上時段:  "+str(clinic_time[2][0])+" ~ "+str(clinic_time[2][1]),
            "color": "#6c757d",
            "margin": "none",
            "size": "lg",
            "weight": "bold"
          }
        ],
        "margin": "md"
      }
    ]
  }
}
  flex_message = FlexSendMessage(
                  alt_text='開診時間資料轉圖片',
                  contents= get_clinic_opentime #json貼在這裡
              )
  return flex_message