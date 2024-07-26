import time
from collections import defaultdict
import re
import subprocess
from slack_alert import send_slack_notification

# Path to the Apache access log file
LOG_FILE_PATH = '/opt/lampp/logs/access_log'
name="DoS (Denial of Service) attack"

# Thresholds
REQUEST_THRESHOLD = 20
TIMEFRAME = 60  # Timeframe in seconds (1 minute)
COOLDOWN_PERIOD = 60  # Cooldown period in seconds (1 minute)

# Dictionary to store request counts: { (ip_address, endpoint): [timestamps] }
request_counts = defaultdict(list)
# Dictionary to store the last alert time for each IP address
last_alert_time = {}

def parse_log_line(line):
    """ Parse a log line and return the IP address and endpoint if valid. """
    match = re.match(r'(\d+\.\d+\.\d+\.\d+) - - \[.*?\] "GET (.+?) HTTP/1.1" \d+ \d+', line)
    if match:
        ip_address, endpoint = match.groups()
        return ip_address, endpoint
    return None, None

def block_ip_address(ip_address):
    """ Block the IP address using iptables. """
    try:
        subprocess.run(['sudo', 'iptables', '-A', 'INPUT', '-s', ip_address, '-j', 'DROP'], check=True)
        print(f"IP address {ip_address} has been blocked.")
        send_slack_notification(ip_address, name, "")
    except subprocess.CalledProcessError as e:
        print(f"Failed to block IP address {ip_address}: {e}")

def check_for_dos(ip_address, endpoint):
    """ Check if the number of requests from the same IP to the same endpoint exceeds the threshold. """
    key = (ip_address, endpoint)
    current_time = time.time()
    
    # Clean up old timestamps
    request_counts[key] = [timestamp for timestamp in request_counts[key] if current_time - timestamp <= TIMEFRAME]
    
    # Add new request timestamp
    request_counts[key].append(current_time)
    
    # Check if the request count exceeds the threshold and cooldown period has passed
    if len(request_counts[key]) > REQUEST_THRESHOLD:
        if ip_address not in last_alert_time or current_time - last_alert_time[ip_address] > COOLDOWN_PERIOD:
            last_alert_time[ip_address] = current_time
            request_count = len(request_counts[key])
            print(f"Alert! Potential DoS attack from IP address {ip_address}. Count: {request_count}")
            block_ip_address(ip_address)
            return True
    return False

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
            
            ip_address, endpoint = parse_log_line(line)
            if ip_address and endpoint:
                if check_for_dos(ip_address, endpoint):
                    # Optionally, you can perform additional actions or logging here
                    pass

if __name__ == "__main__":
    monitor_log_file()
