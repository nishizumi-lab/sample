import pymsteams

# 作成したIncoming WebhookのURLを指定
incoming_webhook_url = "XXXXXXXX"

# 送信するメッセージ
send_message_title = "メッセージのタイトル"
send_message_body = "メッセージの本文"

# メッセージを送信
teams = pymsteams.connectorcard(incoming_webhook_url)
teams.title(send_message_title)
teams.text(send_message_body)
teams.send()