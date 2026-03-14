# slack.py

import requests
import json

def send_slack_alert_manual(error_title, count, timestamp):
    url = "https://slack.com/api/chat.postMessage"
    bot_token = "xoxb-your-slack-token"
    
    # Fixed 'Content' typo
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {bot_token}" # Best practice: Auth in header
    }
    
    payload = {
        "channel": "C12345678",
        "blocks": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": "Manual API Alert"} # Added }
            },
            {
                "type": "section",
                "fields":[
                    {"type": "mrkdwn", "text": f"*Error:* '{error_title}'"}, # Added }
                    {"type": "mrkdwn", "text": f"*Count:* {count}"}
                ]
            },
            {
                "type": "context",
                "elements": [
                    {"type": "mrkdwn", "text": f"Sent via 'requests' at {timestamp}"}
                ]
            }
        ]
    }

    # json.dumps() turns the dictionary into the string: '{"channel": "C12345678", ...}'
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code != 200:
        print(f"Network error: {response.status_code}")
    else:
        result = response.json() # Converts Slack's string back to a Python Dict
        if not result.get("ok"):
            print(f"Slack logic error: {result.get('error')}")
        else:
            print("Successful send.")
            return result['ts']
