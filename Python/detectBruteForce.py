import time
from collections import defaultdict
import re
import subprocess
from slack_alert import send_slack_notification

# Path to the Apache access log file
LOG_FILE_PATH = '/opt/lampp/logs/access_log'
name = "Brute Force attack"

# Thresholds
ATTEMPT_THRESHOLD = 5
TIMEFRAME = 60  # Timeframe in seconds (1 minute)
COOLDOWN_PERIOD = 60  # Cooldown period in seconds (1 minute)

# Dictionary to store request counts: { (ip_address): [timestamps] }
request_counts = defaultdict(list)
# Dictionary to store the last alert time for each IP address
last_alert_time = defaultdict(lambda: 0)

def parse_log_line(line):
    """ Parse a log line and return the IP address and status (success/failure). """
    match = re.match(r'(\d+\.\d+\.\d+\.\d+) - - \[.*?\] "GET /DVWA/vulnerabilities/brute/\?username=[^&]+&password=[^&]+&Login=Login HTTP/1.1" \d+ (\d+)', line)
    if match:
        ip_address = match.group(1)
        response_size = int(match.group(2))  # Capture the response size
        success = response_size > 4300  # Adjust the size threshold based on what your logs show for success
        return ip_address, success
    return None, False

def block_ip_address(ip_address):
    """ Block the IP address using iptables. """
    try:
        subprocess.run(['sudo', 'iptables', '-A', 'INPUT', '-s', ip_address, '-j', 'DROP'], check=True)
        print(f"IP address {ip_address} has been blocked.")
        send_slack_notification(ip_address, name, "")
    except subprocess.CalledProcessError as e:
        print(f"Failed to block IP address {ip_address}: {e}")

def check_for_brute_force(ip_address, success):
    """ Check if the IP address is performing a brute force attack, and block if necessary. """
    if success:
        return False  # Skip successful attempts

    current_time = time.time()
    
    # Clean up old timestamps
    request_counts[ip_address] = [timestamp for timestamp in request_counts[ip_address] if current_time - timestamp <= TIMEFRAME]
    
    # Add new request timestamp
    request_counts[ip_address].append(current_time)
    
    # Check if the request count exceeds the threshold and cooldown period has passed
    if len(request_counts[ip_address]) > ATTEMPT_THRESHOLD:
        if current_time - last_alert_time[ip_address] > COOLDOWN_PERIOD:
            last_alert_time[ip_address] = current_time
            print(f"Alert! Potential Brute force attack from IP address {ip_address}.", flush=True)
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
            
            ip_address, success = parse_log_line(line)
            if ip_address:
                if check_for_brute_force(ip_address, success):
                    pass

if __name__ == "__main__":
    monitor_log_file()
