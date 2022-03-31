from ast import expr_context
from tkinter import S
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('017Ztelu1iHkntih/JEUALbYGT3WWvvDq4xxr9+JSVIQRHoFsz7zYCMp9smy1RKXASCdusmlELRDkPikzWtNb4PBvCF8yNZuMANxhcEMs9CYWs3/qPSb8X5AMkyqpndr3zLXEHK+OYowJ/cTnvcE7AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f0fcee652263244dfccb18e4001c4f49')

import json
import requests

data = requests.get("https://data.epa.gov.tw/api/v1/aqx_p_432?limit=1000&api_key=9be7b239-557b-4c10-9775-78cadfc555e9&format=json").json()

a = data["records"][0]["SiteName"]
print(a)


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)

def handle_message(event):
    msg = event.message.text
    #s = "笑死"
    if msg=="help":
        print()
    try:
        int(msg)
        s = data["records"][msg]["SiteName"]
    except:
        s = "輸入錯誤，請重新輸入"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=s))


if __name__ == "__main__":
    app.run()