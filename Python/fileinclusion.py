import time
import re
import subprocess
from slack_alert import send_slack_notification

# Path to the Apache access log file
LOG_FILE_PATH = '/opt/lampp/logs/access_log'
name = "File Inclusion"
name_rfi = "Remote File Inclusion"
name_lfi = "Local File Inclusion"

# Regular expression pattern for remote file inclusion
rfi_pattern = re.compile(r'(http|https)://', re.IGNORECASE)

# Allowed files for local file inclusion
allowed_files = {'file1.php', 'file2.php', 'file3.php'}

def detect_rfi(line):
    """Detect Remote File Inclusion (RFI) attempts in the log line."""
    match = rfi_pattern.search(line)
    if match:
        ip_match = re.match(r'(\d+\.\d+\.\d+\.\d+)', line)
        if ip_match:
            ip_address = ip_match.group(1)
            accessed_link = match.group(0)
            attack_details = f"Attack Type: {name_rfi}\nAccessed: {accessed_link}"
            alert_message = f"Alert! Potential File Inclusion detected from IP address {ip_address}\n{attack_details}"
            print(alert_message)
            send_slack_notification(ip_address, name, attack_details)
            return ip_address, attack_details
    return None, None

def detect_lfi(line):
    """Detect Local File Inclusion (LFI) attempts in the log line."""
    lfi_match = re.search(r'/DVWA/vulnerabilities/fi/\?page=([^& ]+)', line)
    if lfi_match:
        file_name = lfi_match.group(1)
        if file_name not in allowed_files:
            ip_match = re.match(r'(\d+\.\d+\.\d+\.\d+)', line)
            if ip_match:
                ip_address = ip_match.group(1)
                accessed_file = lfi_match.group(0)
                attack_details = f"Attack Type: {name_lfi}\nAccessed: {accessed_file}"
                alert_message = f"Alert! Potential File Inclusion detected from IP address {ip_address}\n{attack_details}"
                print(alert_message)
                send_slack_notification(ip_address, name, attack_details)
                return ip_address, attack_details
    return None, None

def block_ip_address(ip_address, attack_type):
    """Block the IP address using iptables."""
    try:
        subprocess.run(['sudo', 'iptables', '-A', 'INPUT', '-s', ip_address, '-j', 'DROP'], check=True)
        print(f"IP address {ip_address} has been blocked due to {attack_type}.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to block IP address {ip_address}: {e}")
    except Exception as e:
        print(f"Error sending Slack notification: {e}")

def monitor_log_file():
    """Continuously monitor the log file for new entries."""
    with open(LOG_FILE_PATH, 'r') as log_file:
        # Move to the end of the file
        log_file.seek(0, 2)
        
        while True:
            line = log_file.readline()
            if not line:
                # Sleep briefly to wait for new log entries
                time.sleep(0.1)
                continue
            
            # Check for RFI
            ip_address, attack_details = detect_rfi(line)
            if ip_address:
                block_ip_address(ip_address, name_rfi)
                continue
            
            # Check for LFI
            ip_address, attack_details = detect_lfi(line)
            if ip_address:
                block_ip_address(ip_address, name_lfi)

if __name__ == "__main__":
    monitor_log_file()
