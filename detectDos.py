import re  # Import regular expression module for parsing log lines
import subprocess  # Import subprocess for running shell commands
from collections import defaultdict  # Import defaultdict for efficient data handling
from datetime import datetime, timedelta  # Import datetime for timestamp manipulation
import requests  # Import requests for sending HTTP requests

def parse_log_line(line):
    # Regular expression pattern to extract IP address, timestamp, HTTP method, and URL from log line
    pattern = r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) .* \[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}) \+\d{4}\] "(GET|POST|PUT|DELETE) (\S+) HTTP/\d\.\d"'
    match = re.search(pattern, line)
    if match:
        # Extract matched groups
        ip_address = match.group(1)
        timestamp_str = match.group(2)
        http_method = match.group(3)
        url = match.group(4)

        # Convert timestamp string to datetime object
        timestamp = datetime.strptime(timestamp_str, '%d/%b/%Y:%H:%M:%S')
        return ip_address, http_method, url, timestamp
    return None, None, None, None  # Return None if no match found

def monitor_log(file_path, threshold=20):
    # Initialize dictionaries to store IP request counts and timestamps, and a set for blocked IPs
    ip_request_counts = defaultdict(lambda: defaultdict(int))
    ip_timestamps = defaultdict(list)
    blocked_ips = set()

    # Open a subprocess to tail the log file continuously
    with subprocess.Popen(['tail', '-f', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        while True:
            line = proc.stdout.readline()  # Read each line from the log file
            if not line:
                break  # Break if no more lines are read
            
            line = line.decode('utf-8').strip()  # Decode bytes to string and strip newline characters
            ip_address, http_method, url, timestamp = parse_log_line(line)  # Parse log line to extract relevant data
            
            if ip_address and http_method == "GET":
                # Increment request count and store timestamp
                ip_request_counts[ip_address][timestamp] += 1
                ip_timestamps[ip_address].append(timestamp)
                # Check for potential DoS attack based on thresholds
                check_dos_attack(ip_address, ip_request_counts, ip_timestamps, blocked_ips, threshold)

def check_dos_attack(ip_address, ip_request_counts, ip_timestamps, blocked_ips, threshold):
    if ip_address in blocked_ips:
        return  # Skip further checks if IP is already blocked

    current_time = datetime.now()
    window_time = current_time - timedelta(minutes=1)  # Define a 1-minute time window
    
    # Filter recent requests within the defined time window
    recent_requests = [t for t in ip_timestamps[ip_address] if t > window_time]
    
    # If requests exceed the threshold, trigger a DoS alert
    if len(recent_requests) > threshold:
        print("-------------------------------------------------Alert! Potential DoS attack detected-------------------------------------------------")
        print(f"IP Address: {ip_address}")
        print(f"Number of GET requests in the last minute: {len(recent_requests)}")
        block_ip(ip_address)  # Block the IP address using iptables
        blocked_ips.add(ip_address)  # Add IP to blocked set to avoid repeated blocking
        ip_request_counts[ip_address].clear()  # Clear request counts for the blocked IP
        ip_timestamps[ip_address].clear()  # Clear timestamps for the blocked IP

        # Send alert to Slack
        send_slack_alert(ip_address)

def block_ip(ip_address):
    # Construct and execute iptables command to block the IP address
    command = f"sudo iptables -A INPUT -s {ip_address} -j DROP"
    subprocess.run(command, shell=True)
    
    # Print a message indicating the IP address is blocked
    print(f"{ip_address} is blocked.")

def send_slack_alert(ip_address):
    # Define Slack webhook URL and message format
    webhook_url = 'https://hooks.slack.com/services/T07AQ7E6RRP/B07A4UL637G/vYDnwE'
    message = {
        'text': f"Alert! Potential DoS attack from {ip_address}."
    }
    # Send HTTP POST request to Slack webhook
    response = requests.post(webhook_url, json=message)
    if response.status_code != 200:
        raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")

if __name__ == "__main__":
    log_file = "/opt/lampp/logs/access_log"
    monitor_log(log_file, threshold=20)  # Start monitoring the log file with a specified threshold
