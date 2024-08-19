import requests
import json
import subprocess
import sys
import pickle
from collections import defaultdict
from datetime import datetime, timedelta
import os

# Define your API key and endpoint
api_key = 'apikey'
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
attempts_reset_time = 30  # in seconds
block_duration = 300  # in seconds (5 minutes)
attempts_file = "/var/tmp/attempts.pkl"

def load_attempts():
    try:
        with open(attempts_file, "rb") as f:
            attempts = pickle.load(f)
            # Ensure the loaded data structure is as expected
            for ip, data in attempts.items():
                if not isinstance(data, dict) or 'count' not in data or 'last_attempt' not in data:
                    attempts[ip] = {'count': 0, 'last_attempt': datetime.min}
            return attempts
    except FileNotFoundError:
        return defaultdict(lambda: {'count': 0, 'last_attempt': datetime.min})

def save_attempts(attempts):
    with open(attempts_file, "wb") as f:
        pickle.dump(attempts, f)

def block_ip(ip):
    try:
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        print(f"Blocked IP: {ip}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to block IP {ip}: {e}")

def restart_web_server():
    try:
        subprocess.run(["sudo", "systemctl", "restart", "apache2"], check=True)
        print("Web server restarted successfully, resetting DVWA security level to 'impossible'.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to restart web server: {e}")

def invalidate_sessions():
    session_path = "/var/lib/php/sessions"
    try:
        for session_file in os.listdir(session_path):
            file_path = os.path.join(session_path, session_file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print("Invalidated all sessions.")
    except Exception as e:
        print(f"Failed to invalidate sessions: {e}")

def handle_ip(ip):
    attempts = load_attempts()
    print(f"Handling IP: {ip}")
    
    current_time = datetime.now()
    last_attempt = attempts[ip]['last_attempt']
    
    if (current_time - last_attempt).seconds > attempts_reset_time:
        attempts[ip]['count'] = 0
    
    attempts[ip]['count'] += 1
    attempts[ip]['last_attempt'] = current_time
    
    print(f"Attempts for {ip}: {attempts[ip]['count']}")
    save_attempts(attempts)
    
    if attempts[ip]['count'] >= threshold:
        send_email()
        block_ip(ip)
        attempts[ip]['count'] = 0  # Reset count after blocking
        save_attempts(attempts)
        
        # Invalidate sessions and restart the web server
        invalidate_sessions()
        restart_web_server()

        # Schedule unblocking the IP after block_duration
        unblock_time = current_time + timedelta(seconds=block_duration)
        unblock_command = f"sudo /usr/bin/python3 /usr/local/bin/unblock_ip.py {ip}"
        subprocess.run(["at", unblock_time.strftime('%H:%M')], input=unblock_command, text=True)

if __name__ == "__main__":
    print(f"Arguments received: {sys.argv}")
    if len(sys.argv) < 2:
        print("Usage: python send_swatch_email.py <log_line>")
        sys.exit(1)

    log_line = ' '.join(sys.argv[1:])
    print(f"Log line: {log_line}")
    
    # Extract the IP address from the log line
    ip = log_line.split(' ')[0]
    handle_ip(ip)
