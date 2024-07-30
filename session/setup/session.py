import re
import subprocess
from datetime import datetime
import requests

# Paths to the log file and output alert log file
LOG_FILE = 'session_user_access.log'
ALERT_LOG_FILE = 'session_alerts.log'

# Function to parse a log line and extract relevant details
def parse_log_line(line):
    # Example log format: 127.0.0.1 - - [12/Feb/2023:12:34:56 +0000] "GET /index.php HTTP/1.1" 200 1234
    pattern = r'^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+)\s?(HTTP/\d\.\d)?" (\d{3}) (\d+)'
    match = re.match(pattern, line)
    if match:
        ip_address = match.group(1)
        method = match.group(5)
        url = match.group(6)
        status_code = match.group(8)
        return ip_address, method, url, status_code
    return None, None, None, None

# Function to monitor the log file for suspicious activities
def monitor_log(file_path):
    with subprocess.Popen(['tail', '-f', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True) as proc:
        for line in iter(proc.stdout.readline, ''):
            line = line.strip()
            if line:
                ip_address, method, url, status_code = parse_log_line(line)
                if ip_address and method == "GET":
                    detect_session_attacks(ip_address, url, status_code)

# Function to detect session attacks based on parsed log details
def detect_session_attacks(ip_address, url, status_code):
    if detect_session_hijacking(url):
        handle_alert("Session Hijacking Attack detected", ip_address, url)
    elif detect_session_replay(url):
        handle_alert("Session Replay Attack detected", ip_address, url)
    elif detect_session_sidejacking(ip_address):
        handle_alert("Session Sidejacking Attack detected", ip_address, url)

# Function to detect Session Hijacking attacks
def detect_session_hijacking(url):
    # Example detection: Check for unusual session IDs or access patterns
    if 'sessionid=' in url or 'token=' in url:
        return True
    return False

# Function to detect Session Replay attacks
def detect_session_replay(url):
    # Example detection: Check for repeated or expired session tokens/IDs
    if 'replay=' in url or 'expired=' in url:
        return True
    return False

# Function to detect Session Sidejacking attacks
def detect_session_sidejacking(ip_address):
    # Example detection: Check for suspicious cross-user session activity
    if 'session-hijack' in ip_address:
        return True
    return False

# Function to handle alerts (e.g., logging, sending alerts via Slack/email)
def handle_alert(alert_message, ip_address, url):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    alert_details = f"{timestamp} - {alert_message} from {ip_address} requesting {url}"
    print(alert_details)
    write_to_alert_log(alert_details)
    send_slack_alert(alert_message, ip_address, url)

# Example function to write alerts to a log file
def write_to_alert_log(alert_details):
    with open(ALERT_LOG_FILE, 'a') as f:
        f.write(alert_details + '\n')

# Example function to send alerts to Slack
def send_slack_alert(alert_message, ip_address, url):
    webhook_url = 'https://hooks.slack.com/services/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'
    payload = {'text': f"{alert_message} from {ip_address} requesting {url}"}
    response = requests.post(webhook_url, json=payload)
    if response.status_code != 200:
        raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")

# Main function to start monitoring the log file
if __name__ == "__main__":
    monitor_log(LOG_FILE)
