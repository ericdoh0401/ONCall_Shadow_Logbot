# slack.py

import requests
import json

def send_slack_alert_manual(error_title, count, timestamp, bot_token, channel):
    url = "https://slack.com/api/chat.postMessage"
    
    # Fixed 'Content' typo
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {bot_token}" # Best practice: Auth in header
    }
    
    payload = {
        "channel": channel,
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
                    {"type": "mrkdwn", "text": f"Sent via API 'requests' at {timestamp}"}
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
            
if __name__ == "__main__":
    send_slack_alert_manual("ERROR", 50, "2024-01-01T00:00:00Z", "your-bot-token", "C123456")
