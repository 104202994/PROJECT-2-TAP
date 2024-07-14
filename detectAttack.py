import re
import subprocess
from collections import defaultdict
from datetime import datetime, timedelta
import requests
import time

def parse_log_line(line):
    pattern = r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) .* \[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}) \+\d{4}\] "(GET|POST|PUT|DELETE) (\S+) HTTP/\d\.\d"'
    match = re.search(pattern, line)
    if match:
        ip_address = match.group(1)
        timestamp_str = match.group(2)
        http_method = match.group(3)
        url = match.group(4)

        timestamp = datetime.strptime(timestamp_str, '%d/%b/%Y:%H:%M:%S')
        return ip_address, http_method, url, timestamp
    return None, None, None, None

def monitor_log(file_path, threshold=20):
    ip_request_counts = defaultdict(lambda: defaultdict(int))
    ip_timestamps = defaultdict(list)
    blocked_ips = set()

    with subprocess.Popen(['tail', '-f', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        while True:
            line = proc.stdout.readline()
            if not line:
                break
            
            line = line.decode('utf-8').strip()
            ip_address, http_method, url, timestamp = parse_log_line(line)
            
            if ip_address and http_method == "GET":
                ip_request_counts[ip_address][timestamp] += 1
                ip_timestamps[ip_address].append(timestamp)
                check_dos_attack(ip_address, ip_request_counts, ip_timestamps, blocked_ips, threshold)
                check_brute_force(ip_address, ip_timestamps, blocked_ips)

def check_dos_attack(ip_address, ip_request_counts, ip_timestamps, blocked_ips, threshold):
    if ip_address in blocked_ips:
        return

    current_time = datetime.now()
    window_time = current_time - timedelta(minutes=1)
    
    recent_requests = [t for t in ip_timestamps[ip_address] if t > window_time]
    
    if len(recent_requests) > threshold:
        print("-------------------------------------------------Alert! Potential DoS attack detected-------------------------------------------------")
        print(f"IP Address: {ip_address}")
        print(f"Number of GET requests in the last minute: {len(recent_requests)}")
        block_ip(ip_address)
        blocked_ips.add(ip_address)
        ip_request_counts[ip_address].clear()
        ip_timestamps[ip_address].clear()

        # Send alert to Slack
        send_slack_alert(ip_address, "DoS attack detected")

def check_brute_force(ip_address, ip_timestamps, blocked_ips, threshold=10, time_window=1):
    if ip_address in blocked_ips:
        return

    timestamps = ip_timestamps[ip_address]
    if len(timestamps) >= threshold:
        timestamps.sort()
        if (timestamps[-1] - timestamps[-threshold]).seconds <= time_window:
            print("-------------------------------------------------Alert! Potential Brute Force attack detected-------------------------------------------------")
            print(f"IP Address: {ip_address}")
            block_ip(ip_address)
            blocked_ips.add(ip_address)
            ip_timestamps[ip_address].clear()

            # Send alert to Slack
            send_slack_alert(ip_address, "Brute force attack detected")

def block_ip(ip_address):
    command = f"sudo iptables -A INPUT -s {ip_address} -j DROP"
    subprocess.run(command, shell=True)
    
    # Print a message indicating the IP address is blocked
    print(f"{ip_address} is blocked.")

def send_slack_alert(ip_address, alert_type):
    webhook_url = 'WEbhook'
    message = {
        'text': f"Alert! {alert_type} from {ip_address}."
    }
    response = requests.post(webhook_url, json=message)
    if response.status_code != 200:
        raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")

if __name__ == "__main__":
    log_file = "/opt/lampp/logs/access_log"
    monitor_log(log_file, threshold=20)
