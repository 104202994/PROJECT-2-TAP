import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta
import subprocess

# Path to the Slack alert script
ALERT_SCRIPT = '/home/nil/Desktop/Swatch/scripts/send_slack_alert.py'

# Threshold for brute force detection
THRESHOLD = 5
TIME_WINDOW = 60  # 1 minute in seconds
COOLDOWN_PERIOD = 300  # 5 minutes in seconds

login_attempts = defaultdict(list)
last_alert_time = defaultdict(lambda: datetime.min)
blocked_ips = set()
pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "GET \/DVWA\/vulnerabilities\/brute\/\?username=admin&password=.*"')

def send_slack_alert(message):
    subprocess.run(['python3', ALERT_SCRIPT, message])

def block_ip(ip):
    if ip not in blocked_ips:
        # Execute the iptables command to block the IP
        subprocess.run(['sudo', 'iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP'])
        blocked_ips.add(ip)
        return True
    return False

def process_line(line):
    match = pattern.match(line)
    if match:
        ip = match.group(1)
        timestamp_str = match.group(2).split()[0]
        timestamp = datetime.strptime(timestamp_str, "%d/%b/%Y:%H:%M:%S")
        login_attempts[ip].append(timestamp)
        # Only consider recent attempts (within the last minute)
        recent_attempts = [attempt for attempt in login_attempts[ip] if datetime.now() - attempt <= timedelta(seconds=TIME_WINDOW)]
        login_attempts[ip] = recent_attempts  # Keep only recent attempts
        if len(recent_attempts) > THRESHOLD:
            if datetime.now() - last_alert_time[ip] > timedelta(seconds=COOLDOWN_PERIOD):
                # Trigger alert
                blocked = block_ip(ip)
                message = (
                    f"Alert! Potential Brute Force Attempt Detected from IP: *{ip}*\n"
                    
                )
                if blocked:
                    message += f"```{'IP Address Blocked'}```"
                send_slack_alert(message)
                last_alert_time[ip] = datetime.now()

# Read from standard input
for line in sys.stdin:
    process_line(line)
