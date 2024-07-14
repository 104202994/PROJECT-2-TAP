import re
import time
from collections import defaultdict, deque
from datetime import datetime, timedelta
import subprocess
import requests  # Import requests library for HTTP requests

# Function to send alert to Slack channel
def send_slack_alert(webhook_url, attack_name, ip_address):
    message = f"Alert! Potential {attack_name} from {ip_address}"
    payload = {
        "text": message
    }
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()  # Raise exception for bad responses (4xx or 5xx)
        print("Slack alert sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Slack alert: {e}")

def detect_brute_force(log_file_path):
    suspicious_pattern = r'/vulnerabilities/brute/\?username=([^&]*)&password=([^&]*)&Login=Login'
    max_attempts = 5
    detection_window = timedelta(minutes=1)
    ip_username_attempts = defaultdict(lambda: defaultdict(lambda: deque(maxlen=max_attempts)))
    blocked_ips = set()
    
    # Infinite loop to continuously monitor the log file
    while True:
        try:
            with open(log_file_path, 'r') as file:
                # Move to the end of the file
                file.seek(0, 2)
                while True:
                    line = file.readline()
                    if not line:
                        time.sleep(0.1)  # Wait briefly for new data
                        continue
                    
                    match = re.search(suspicious_pattern, line)
                    if match:
                        username = match.group(1)
                        ip_address = line.split()[0]
                        current_time = datetime.strptime(line.split()[3][1:], '%d/%b/%Y:%H:%M:%S')
                        
                        # Check if IP is blocked
                        if ip_address in blocked_ips:
                            continue
                        
                        # Check if username has exceeded max_attempts within detection_window for this IP address
                        if ip_username_attempts[ip_address][username] and current_time - ip_username_attempts[ip_address][username][0] > detection_window:
                            ip_username_attempts[ip_address][username].clear()  # Clear deque if window expired
                        
                        ip_username_attempts[ip_address][username].append(current_time)
                        
                        if len(ip_username_attempts[ip_address][username]) >= max_attempts:
                            if ip_address not in blocked_ips:
                                # Print message indicating potential brute force attack
                                print(f"Potential brute force attack detected from {ip_address}")
                                
                                # Send Slack alert
                                webhook_url = 'WEBHOOK'
                                attack_name = "Brute Force Attack"
                                send_slack_alert(webhook_url, attack_name, ip_address)
                                
                                block_ip(ip_address, blocked_ips)
                                blocked_ips.add(ip_address)  # Add IP to blocked set after blocking
        
        except FileNotFoundError:
            print(f"Log file '{log_file_path}' not found. Waiting for it to be created...")
            time.sleep(5)  # Wait for the log file to be created

def block_ip(ip_address, blocked_ips):
    command = f"sudo iptables -A INPUT -s {ip_address} -j DROP"
    subprocess.run(command, shell=True)
    
    # Print a message indicating the IP address is blocked
    print(f"{ip_address} is blocked.")

if __name__ == "__main__":
    log_file_path = '/opt/lampp/logs/access_log'  # Replace with your XAMPP log file path
    detect_brute_force(log_file_path)
