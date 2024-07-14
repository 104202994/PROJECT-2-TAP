import re
import time
import subprocess
import requests

# Path to the Apache access log file
log_file = '/opt/lampp/logs/access_log'

# Slack webhook URL
slack_webhook_url = 'https://hooks.slack.com/services/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'

# Regular expression pattern to detect directory traversal attempts
traversal_pattern = re.compile(r'\.\./|/\.\./|\/\.\../')

# Set to store blocked IPs to avoid blocking multiple times
blocked_ips = set()

def check_directory_traversal(log_line):
    """Check if a log line indicates a directory traversal attempt."""
    if traversal_pattern.search(log_line):
        return True
    return False

def send_slack_alert(ip_address, log_line):
    """Send alert to Slack channel."""
    message = f"Alert! Potential directory traversal detected from IP {ip_address}:\n```{log_line}```"
    payload = {'text': message}
    response = requests.post(slack_webhook_url, json=payload)
    if response.status_code != 200:
        print(f"Failed to send Slack alert: {response.status_code} - {response.text}")

def block_ip(ip_address):
    """Block the IP address using iptables."""
    if ip_address not in blocked_ips:
        command = f"sudo iptables -A INPUT -s {ip_address} -j DROP"
        subprocess.run(command, shell=True)
        blocked_ips.add(ip_address)
        print(f"{ip_address} is blocked.")
        send_slack_alert(ip_address, "IP blocked due to directory traversal attempt.")

def read_logs():
    """Read logs in real-time and check for directory traversal attempts."""
    try:
        with open(log_file, 'r') as f:
            # Start reading from the end of the file
            f.seek(0, 2)
            while True:
                line = f.readline()
                if line:
                    if check_directory_traversal(line):
                        # Extract IP address from log line (assuming common log format)
                        ip_address = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
                        if ip_address:
                            ip_address = ip_address.group()
                            block_ip(ip_address)
                else:
                    time.sleep(0.1)  # Sleep briefly before checking for new lines
    except KeyboardInterrupt:
        print("Stopping log monitoring.")

if __name__ == "__main__":
    read_logs()
