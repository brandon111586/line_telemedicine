import requests
import json

LINE_CHANNEL_ACCESS_TOKEN = 'rTIVtyQMX7seAHTiLsgZZlBKT1qhMw73M0FKKRqHzXgoIsJqy6gKaCTlEVhW6ypYZadFGKmToZkST07VR4BeYs7cpTE2uyKoYa2lvJ1M3t0lZShblDxYriXgVA0G4erj6RifbV1FRYzsWCT+6Vh9eAdB04t89/1O/w1cDnyilFU='

token = LINE_CHANNEL_ACCESS_TOKEN

Authorization_token = "Bearer " + LINE_CHANNEL_ACCESS_TOKEN

headers = {"Authorization":Authorization_token, "Content-Type":"application/json"}

# body = {
#     'size': {'width': 2500, 'height': 1200},   # 設定尺寸
#     'selected': 'true',                        # 預設是否顯示
#     'name': 'aaa',                             # 選單名稱 ( 別名 Alias Id )
#     'chatBarText': '選單 A',                    # 選單在 LINE 顯示的標題
#     'areas':[                                  # 選單內容
#         {
#           'bounds': {'x': 0, 'y': 0, 'width': 830, 'height': 280},
#           'action': {'type': 'postback', 'data':'no-data'}          # 按鈕 A 使用 postback
#         },
#         {
#           'bounds': {'x': 835, 'y': 0, 'width':830, 'height': 640},
#           'action': {'type': 'richmenuswitch', 'richMenuAliasId': 'bbb', 'data':'change-to-bbb'} # 按鈕 B 使用 richmenuswitch
#         },
#         {
#           'bounds': {'x': 1670, 'y': 0, 'width':830, 'height': 640},
#           'action': {'type': 'richmenuswitch', 'richMenuAliasId': 'ccc', 'data':'change-to-ccc'} # 按鈕 C 使用 richmenuswitch
#         }
#     ]
#   }

# req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',
#                        headers=headers,data=json.dumps(body).encode('utf-8'))

# print(req.text)
# {"richMenuId":"richmenu-0e53e3e11969dd6869fcca91de7524c1"}

from linebot import LineBotApi,WebhookHandler

line_bot_api =LineBotApi(token)
# rich_menu_id = "richmenu-0e53e3e11969dd6869fcca91de7524c1"

# path = "line-rich-menu-switch-demo-a.jpg"
# with open(path,'rb') as f:
#     line_bot_api.set_rich_menu_image(rich_menu_id,"image/jpeg",f)

# import requests
# import json

# body = {
#     "richMenuAliasId":"aaa",
#     "richMenuId":"richmenu-0e53e3e11969dd6869fcca91de7524c1"
# }
# req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu/alias',
#                       headers=headers,data=json.dumps(body).encode('utf-8'))
# print(req.text)
# req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/richmenu-0e53e3e11969dd6869fcca91de7524c1', headers=headers)
# print(req.text)

# body = {
#     'size': {'width': 2500, 'height': 1200},   # 設定尺寸
#     'selected': 'true',                        # 預設是否顯示
#     'name': 'bbb',                             # 選單名稱 ( 別名 Alias Id )
#     'chatBarText': '選單 B',                    # 選單在 LINE 顯示的標題
#     'areas':[                                  # 選單內容
#         {
#           'bounds': {'x': 0, 'y': 0, 'width': 830, 'height': 280},
#           'action': {'type': 'richmenuswitch', 'richMenuAliasId': 'aaa', 'data':'change-to-aaa'} # 按鈕 A 使用 richmenuswitch
#         },
#         {
#           'bounds': {'x': 835, 'y': 0, 'width':830, 'height': 640},
#           'action': {'type': 'postback', 'data':'no-data'}          # 按鈕 B 使用 postback
#         },
#         {
#           'bounds': {'x': 1670, 'y': 0, 'width':830, 'height': 640},
#           'action': {'type': 'richmenuswitch', 'richMenuAliasId': 'ccc', 'data':'change-to-ccc'} # 按鈕 C 使用 richmenuswitch
#         }
#     ]
#   }
# req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',
#                       headers=headers,data=json.dumps(body).encode('utf-8'))
# print(req.text)
# {"richMenuId":"richmenu-fa2da41034468a7add42d43ff86d0a3d"}

# line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
# with open("line-rich-menu-switch-demo-b.jpg", 'rb') as f:
#     line_bot_api.set_rich_menu_image("richmenu-fa2da41034468a7add42d43ff86d0a3d", "image/jpeg", f)

# body = {
#     "richMenuAliasId":"bbb",
#     "richMenuId":"richmenu-fa2da41034468a7add42d43ff86d0a3d"
# }
# req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu/alias',
#                       headers=headers,data=json.dumps(body).encode('utf-8'))
# print(req.text)

# req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/richmenu-fa2da41034468a7add42d43ff86d0a3d', headers=headers)

# body = {
#     'size': {'width': 2500, 'height': 1200},   # 設定尺寸
#     'selected': 'true',                        # 預設是否顯示
#     'name': 'ccc',                             # 選單名稱 ( 別名 Alias Id )
#     'chatBarText': '選單 C',                    # 選單在 LINE 顯示的標題
#     'areas':[                                  # 選單內容
#         {
#           'bounds': {'x': 0, 'y': 0, 'width': 830, 'height': 280},
#           'action': {'type': 'richmenuswitch', 'richMenuAliasId': 'aaa', 'data':'change-to-aaa'} # 按鈕 A 使用 richmenuswitch
#         },
#         {
#           'bounds': {'x': 835, 'y': 0, 'width':830, 'height': 640},
#           'action': {'type': 'richmenuswitch', 'richMenuAliasId': 'bbb', 'data':'change-to-ccc'} # 按鈕 B 使用 richmenuswitch
#         },
#         {
#           'bounds': {'x': 1670, 'y': 0, 'width':830, 'height': 640},
#           'action': {'type': 'postback', 'data':'no-data'}          # 按鈕 C 使用 postback
#         }
#     ]
#   }
# req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',
#                       headers=headers,data=json.dumps(body).encode('utf-8'))
# print(req.text)

# with open("line-rich-menu-switch-demo-c.jpg", 'rb') as f:
#     line_bot_api.set_rich_menu_image("richmenu-9a16b2bea902c88707014cea431b5888", "image/jpeg", f)


# body = {
#     "richMenuAliasId":"ccc",
#     "richMenuId":"richmenu-9a16b2bea902c88707014cea431b5888"
# }
# req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu/alias',
#                       headers=headers,data=json.dumps(body).encode('utf-8'))

# req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/richmenu-9a16b2bea902c88707014cea431b5888', headers=headers)
rich_menu_list = line_bot_api.get_rich_menu_list()
print(len(rich_menu_list))

