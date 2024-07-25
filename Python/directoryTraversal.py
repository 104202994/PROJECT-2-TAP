import time
import re
import subprocess
import requests
from slack_alert import send_slack_notification

# Path to the Apache access log file
LOG_FILE_PATH = '/opt/lampp/logs/access_log'
name="Directory Traversal"

# Regular expression patterns for directory traversal
traversal_patterns = [
    re.compile(r'\.\./'),  # ../ pattern
    re.compile(r'\.+/../'),  # .+/.. pattern
    re.compile(r'%2e%2e%2f', re.IGNORECASE),  # URL encoded ../
    re.compile(r'%252e%252e%252f', re.IGNORECASE),  # Double URL encoded ../
    re.compile(r'%c0%af', re.IGNORECASE),  # UTF-8/16 encoding
    re.compile(r'%c1%1c', re.IGNORECASE)   # UTF-8/16 encoding
]

def parse_log_line(line):
    """ Parse a log line and return the IP address if it matches directory traversal patterns. """
    for pattern in traversal_patterns:
        if pattern.search(line):
            match = re.match(r'(\d+\.\d+\.\d+\.\d+)', line)
            if match:
                ip_address = match.group(1)
                return ip_address
    return None

def block_ip_address(ip_address):
    """ Block the IP address using iptables. """
    try:
        subprocess.run(['sudo', 'iptables', '-A', 'INPUT', '-s', ip_address, '-j', 'DROP'], check=True)
        print(f"IP address {ip_address} has been blocked.")
        send_slack_notification(ip_address, name)
    except subprocess.CalledProcessError as e:
        print(f"Failed to block IP address {ip_address}: {e}")
    except Exception as e:
        print(f"Error sending Slack notification: {e}")

def monitor_log_file():
    """ Continuously monitor the log file for new entries. """
    with open(LOG_FILE_PATH, 'r') as log_file:
        # Move to the end of the file
        log_file.seek(0, 2)
        
        while True:
            line = log_file.readline()
            if not line:
                # Sleep briefly to wait for new log entries
                time.sleep(0.1)
                continue
            
            ip_address = parse_log_line(line)
            
            if ip_address:
                print(f"Alert! Potential Directory Traversal attempted from IP address {ip_address}.")
                block_ip_address(ip_address)

if __name__ == "__main__":
    monitor_log_file()
