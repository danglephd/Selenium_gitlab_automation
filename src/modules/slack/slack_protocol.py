# from slack_webhook import *
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
except  Exception as error:
    print("Main, Environment variable does not exist: ",  type(error).__name__, "–", error)

def send_survey(user, text, block=None, channel = CHANNEL_ID):
    print('>>>send_survey ', user, text, block, channel)
    # Add try catch error
    try:
        slack_client.api_call(
            # api_method="chat.postMessage", json={"channel": channel, "blocks": json.dumps(block), "text": block}
            api_method="chat.postMessage", json={"channel": channel, "blocks": block or None, "text": text}
        )
    except Exception as e:
        print("Error sending message: {}".format(e))

def read_blocks(issue_obj_list, issue_finished_list, is_finishing=False, is_creating=False):
    issue_summary = "*Collected {0} issue(s):*\n{1}"
    finish_summary = "*Finish {0} issue(s):*"

    data = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":mega: RPA Process completed success. :rocket::rocket:"
            }
        }
    ]

    if is_finishing:
        finish_summary = finish_summary.format(len(issue_finished_list))
        data.append(
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": finish_summary
                    }
                ]
            }
        )
        data.append(get_list_issue_by_table(issue_finished_list))

    if is_creating:
        issue_summary = issue_summary.format(len(issue_obj_list), get_list_issue(issue_obj_list))
        data.append(
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": issue_summary
                    }
                ]
            }
        )
    data.append({"type": "divider"})
        
    return data


def get_list_issue(issue_arr):
    txt = ""
    for issue in issue_arr:
        txt = txt + str.format("<{0}|{1}>, ", issue.issue_url,  issue.issue_number)
    return txt

def get_list_issue_by_table(issue_list):
    """
    Hiển thị danh sách issue dưới dạng Slack table object.
    Header 1: Issue URL
    Header 2: Test URL
    Dữ liệu lấy từ issue_list.
    """
    # Tạo header: mỗi dòng là một list các cell
    rows = [[
        {
            "type": "rich_text",
            "elements": [
                {
                    "type": "rich_text_section",
                    "elements": [
                        {
                            "type": "text",
                            "text": "Issue URL",
                            "style": {"bold": True}
                        }
                    ]
                }
            ]
        },
        {
            "type": "rich_text",
            "elements": [
                {
                    "type": "rich_text_section",
                    "elements": [
                        {
                            "type": "text",
                            "text": "Test URL",
                            "style": {"bold": True}
                        }
                    ]
                }
            ]
        }
    ]]

    # Thêm dữ liệu động từ issue_list
    for issue in issue_list:
        rows.append([
            {
                "type": "rich_text",
                "elements": [
                    {
                        "type": "rich_text_section",
                        "elements": [
                            {
                                "type": "link",
                                "url": getattr(issue, "issue_url", ""),
                                "text": str(getattr(issue, "issue_number", getattr(issue, "issue_url", "")))
                            }
                        ]
                    }
                ]
            },
            {
                "type": "rich_text",
                "elements": [
                    {
                        "type": "rich_text_section",
                        "elements": [
                            {
                                "type": "link",
                                "url": getattr(issue, "issue_test_url", ""),
                                "text": str(getattr(issue, "issue_test_number", getattr(issue, "issue_test_url", "")))
                            }
                        ]
                    }
                ]
            }
        ])

    table_object = {
        "type": "table",
        "rows": rows
    }
    return table_object