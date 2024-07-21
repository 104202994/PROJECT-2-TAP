import sys
import requests
import json

# Slack Webhook URL
WEBHOOK_URL = "https://hooks.slack.com/services/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"

def send_slack_alert(message):
    payload = {
        "text": message
    }
    response = requests.post(WEBHOOK_URL, data=json.dumps(payload),
                             headers={'Content-Type': 'application/json'})
    if response.status_code != 200:
        raise ValueError(
            f'Request to Slack returned an error {response.status_code}, the response is:\n{response.text}'
        )

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 send_slack_alert.py <message>")
        sys.exit(1)
    message = sys.argv[1]
    send_slack_alert(message)

