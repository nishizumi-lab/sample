#!/usr/bin/env python
import requests

# Googleチャットに通知するためのクラス
class GoogleChat:
    def __init__(self, webhook_url) -> None:
        self.webhook_url = webhook_url

    def post_text(self, text):
        json_data= { 'text': text }
        requests.post(self.webhook_url,  json_data)

    def post_card(self, title, widgets):
        json_data = {
                'cards': [
                    {
                        'header': {
                            'title': title,
                            # 'subtitle': subtitle,
                        },
                        'sections': [{'widgets': widgets}],
                    }
                ]
            }
        requests.post(self.webhook_url, json = json_data)

webhook_url = "https://chat.googleapis.com/v1/spaces/XXXXXXXXX/messages?key=XXXXXXXXXXX&token=XXXXXXXXXXXXX"

gchat = GoogleChat(webhook_url)

# テキストメッセージを通知
gchat .post_text("Webhook hello!")

# ウィジェットを通知
widgets = [
  {
    'textParagraph': { 'text': "<a href='https://algorithm.joho.info/'>西住工房</a>" }
  }
]
gchat.post_widget("西住工房にログインがありました。", widgets)