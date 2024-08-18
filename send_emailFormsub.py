#!/usr/bin/env python3

import requests
import json


api_key = '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'
endpoint = 'https://api.brevo.com/v3/smtp/email'


email_data = {
    "sender": {"name": "Security Alert", "email": "tapmonitor2024@gmail.com"},
    "to": [{"email": "abhashspko@gmail.com", "name": "Anonymous"}],
    "subject": "Security Alert",
    "htmlContent": "<html><body><h1>Alert</h1><p>This is a security alert notification.</p></body></html>"
}

# Set the headers
headers = {
    'api-key': api_key,
    'Content-Type': 'application/json'
}

# Send the request
response = requests.post(endpoint, headers=headers, data=json.dumps(email_data))

# Print the response
if response.status_code == 201:
    print("Email sent successfully!")
else:
    print(f"Failed to send email: {response.status_code}")
    print(response.text)
