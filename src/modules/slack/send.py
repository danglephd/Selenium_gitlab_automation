from slack_webhook import *

def send_survey(user, text, block=None, channel = CHANNEL_ID):
    print('>>>send_survey ', user, text, block, channel)
    slack_client.api_call(
        # api_method="chat.postMessage", json={"channel": channel, "blocks": json.dumps(block), "text": block}
        api_method="chat.postMessage", json={"channel": channel, "blocks": block or None, "text": text}
    )