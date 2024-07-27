import requests
import json
import subprocess
import sys
import pickle
from collections import defaultdict

# Define your API key and endpoint
api_key = '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'
endpoint = 'https://api.brevo.com/v3/smtp/email'

# Define the email details
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
def send_email():
    try:
        print("Sending email...")
        response = requests.post(endpoint, headers=headers, data=json.dumps(email_data))
        print(f"Response status code: {response.status_code}")
        if response.status_code == 201:
            print("Email sent successfully!")
        else:
            print(f"Failed to send email: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Exception occurred while sending email: {e}")

# Threshold for blocking IPs
threshold = 5
attempts_file = "/var/tmp/attempts.pkl"

def load_attempts():
    try:
        with open(attempts_file, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return defaultdict(int)

def save_attempts(attempts):
    with open(attempts_file, "wb") as f:
        pickle.dump(attempts, f)

def block_ip(ip):
    try:
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        print(f"Blocked IP: {ip}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to block IP {ip}: {e}")

def handle_ip(ip):
    attempts = load_attempts()
    print(f"Handling IP: {ip}")
    attempts[ip] += 1
    print(f"Attempts for {ip}: {attempts[ip]}")
    save_attempts(attempts)
    if attempts[ip] >= threshold:
        send_email()
        block_ip(ip)

if __name__ == "__main__":
    print(f"Arguments received: {sys.argv}")
    if len(sys.argv) != 2:
        print("Usage: python send_swatch_email.py <ip_address>")
        sys.exit(1)

    ip = sys.argv[1]
    handle_ip(ip)
