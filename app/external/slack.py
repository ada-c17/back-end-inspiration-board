import os
import requests

TOKEN = os.environ.get("SLACK_BOT_TOKEN")

def notify_card_created(card_message):
    data = {
        "channel": "test-channel",
        "text": f"Someone just created a card {card_message}"
    }

    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }

    requests.post('https://slack.com/api/chat.postMessage', data = data, headers = headers)
    print(TOKEN)
