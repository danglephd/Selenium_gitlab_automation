import json
import os
from slackeventsapi import SlackEventAdapter
from slack_sdk import WebClient
from slack_sdk.webhook import WebhookClient
from dotenv import load_dotenv

try:
    load_dotenv()
    # SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]

    # # Create a SlackClient for your bot to use for Web API requests
    SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
    # SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
    CHANNEL_ID = os.environ["CHANNEL_ID"]
    SLACK_HOOK = os.environ["SLACK_HOOK"]
    slack_client = WebClient(SLACK_BOT_TOKEN)
except KeyError:
    print("Environment variable does not exist", KeyError)

# slack = WebhookClient(
#     url = SLACK_HOOK
# )
# slack.send(text="Say hello from RPA_IPTP_QA.")


def send_survey(user, text, block=None, channel = CHANNEL_ID):
    print('>>>send_survey ', user, text, block, channel)
    slack_client.api_call(
        # api_method="chat.postMessage", json={"channel": channel, "blocks": json.dumps(block), "text": block}
        api_method="chat.postMessage", json={"channel": channel, "blocks": block or None, "text": text}
    )
    