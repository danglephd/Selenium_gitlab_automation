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

slack = WebhookClient(
    url = SLACK_HOOK
    # https://hooks.slack.com/services/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
)
slack.send(text="Hello, world.")


def send_survey(user, text, channel = CHANNEL_ID):
    # More info: https://api.slack.com/docs/message-menus
    # Send an in-channel reply to the user
    print('>>>send_survey ', user, text, channel)
    slack_client.api_call(
        api_method="chat.postMessage", json={"channel": channel, "text": text}
    )
    