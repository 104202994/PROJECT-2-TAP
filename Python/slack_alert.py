import requests

SLACK_WEBHOOK_URL = 'https://hooks.slack.com/services'

def send_slack_notification(ip_address, name, attack_details):
    """Send a notification to a Slack channel using the webhook URL."""
    message = {
        "text": f"Alert! Potential {name} detected.\n\n```IP address {ip_address} has been blocked.\n{attack_details}```"
    }
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=message)
        if response.status_code != 200:
            print(f"Failed to send Slack notification: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending Slack notification: {e}")
