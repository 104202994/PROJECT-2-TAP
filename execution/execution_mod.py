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
                    detect_execution_attacks(ip_address, url, query_string)

# Function to detect execution attacks based on parsed log details
def detect_execution_attacks(ip_address, url, query_string):
    if detect_rce_deserialization(query_string):
        handle_alert("RCE via Deserialization detected", ip_address, url)
    elif detect_rce_template_injection(query_string):
        handle_alert("RCE via Template Injection detected", ip_address, url)
    elif detect_privilege_escalation(url):
        handle_alert("Privilege Escalation Attempt detected", ip_address, url)
    elif detect_unauthorized_script_execution(url):
        handle_alert("Unauthorized Script Execution detected", ip_address, url)

# Function to detect RCE via Deserialization attempts
def detect_rce_deserialization(query_string):
    if 'serialize(' in query_string and ('php://input' in query_string or 'php://filter' in query_string):
        return True
    return False

# Function to detect RCE via Server-Side Template Injection attempts
def detect_rce_template_injection(query_string):
    if '{{' in query_string or '${' in query_string:
        return True
    return False

# Function to detect Privilege Escalation attempts
def detect_privilege_escalation(url):
    if '../' in url or '/etc/passwd' in url:
        return True
    return False

# Function to detect Unauthorized Script Execution attempts
def detect_unauthorized_script_execution(url):
    if '.sh' in url or '.php' in url:
        return True
    return False

# Function to handle alerts
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
