import re
import subprocess
from datetime import datetime
import requests
from user_defined_regex import USER_DEFINED_REGEX
from log_config import LOG_FILE

# Function to parse a log line and extract relevant details
def parse_log_line(line, pattern):
    match = re.match(pattern, line)
    if match:
        ip_address = match.group(1)
        method = match.group(5)
        url = match.group(6)
        query_string = match.group(7)
        return ip_address, method, url, query_string
    return None, None, None, None

# Function to monitor the log file for suspicious activities
def monitor_log(file_path, pattern):
    with subprocess.Popen(['tail', '-f', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True) as proc:
        for line in iter(proc.stdout.readline, ''):
            line = line.strip()
            if line:
                ip_address, method, url, query_string = parse_log_line(line, pattern)
                if ip_address and method == "GET":
                    detect_injection_attacks(ip_address, url, query_string)

# Function to detect XSS and LDAP Injection attempts based on parsed log details
def detect_injection_attacks(ip_address, url, query_string):
    if detect_xss_reflected(query_string):
        handle_alert("XSS Reflected Attack detected", ip_address, url)
    elif detect_xss_stored(query_string):
        handle_alert("XSS Stored Attack detected", ip_address, url)
    elif detect_xss_dom(query_string):
        handle_alert("XSS DOM-based Attack detected", ip_address, url)
    elif detect_ldap_injection(query_string):
        handle_alert("LDAP Injection Attack detected", ip_address, url)

# Function to detect XSS Reflected attacks
def detect_xss_reflected(query_string):
    if '<script>' in query_string or 'alert(' in query_string:
        return True
    return False

# Function to detect XSS Stored attacks
def detect_xss_stored(query_string):
    if 'script' in query_string:
        return True
    return False

# Function to detect XSS DOM-based attacks
def detect_xss_dom(query_string):
    if 'document.cookie' in query_string or 'location.href' in query_string:
        return True
    return False

# Function to detect LDAP Injection attacks
def detect_ldap_injection(query_string):
    if 'ldap://' in query_string or '(&(objectClass=*)' in query_string:
        return True
    return False

# Function to handle alerts (e.g., logging, sending alerts via Slack/email)
def handle_alert(alert_message, ip_address, url):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    alert_details = f"{timestamp} - {alert_message} from {ip_address} requesting {url}"
    print(alert_details)
    write_to_alert_log(alert_details)
    send_slack_alert(alert_message, ip_address, url)

# Function to write alerts to a log file
def write_to_alert_log(alert_details):
    with open('alert_log.txt', 'a') as f:
        f.write(alert_details + '\n')

# Function to send alerts to Slack
def send_slack_alert(alert_message, ip_address, url):
    webhook_url = 'https://hooks.slack.com/services/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'
    payload = {'text': f"{alert_message} from {ip_address} requesting {url}"}
    response = requests.post(webhook_url, json=payload)
    if response.status_code != 200:
        raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")

# Main function to start monitoring the log file
if __name__ == "__main__":
    monitor_log(LOG_FILE, USER_DEFINED_REGEX)
