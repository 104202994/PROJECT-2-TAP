import re
from datetime import datetime

# Paths to the log file and output alert log file
LOG_FILE = 'injection_user_access.log'
ALERT_LOG_FILE = 'alert_log.txt'

# Default regex pattern to parse log lines (assuming a common log format)
DEFAULT_REGEX = r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "([A-Z]+) (.*?) HTTP/.*?" (\d+) (\d+)'

# Function to parse a log line and extract relevant details
def parse_log_line(line, pattern):
    match = re.match(pattern, line)
    if match:
        ip_address = match.group(1)
        method = match.group(3)
        url = match.group(4)
        query_string = url.split('?')[1] if '?' in url else ''
        return ip_address, method, url, query_string
    return None, None, None, None

# Function to monitor the log file for suspicious activities
def monitor_log(file_path, pattern):
    with open(file_path, 'r') as file:
        for line in file:
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
    elif detect_command_injection(query_string):
        handle_alert("Command Injection detected", ip_address, url)

# Function to detect RCE via Deserialization attempts
def detect_rce_deserialization(query_string):
    return 'serialize(' in query_string and ('php://input' in query_string or 'php://filter' in query_string)

# Function to detect RCE via Server-Side Template Injection attempts
def detect_rce_template_injection(query_string):
    return '{{' in query_string or '${' in query_string

# Function to detect Privilege Escalation attempts
def detect_privilege_escalation(url):
    return '../' in url or '/etc/passwd' in url

# Function to detect Unauthorized Script Execution attempts
def detect_unauthorized_script_execution(url):
    return '.sh' in url or '.php' in url

# Function to detect Command Injection attempts
def detect_command_injection(query_string):
    command_patterns = ['ls', 'cd', 'sudo', 'cat', 'rm', 'mv', 'cp', 'wget', 'curl']
    return any(command in query_string for command in command_patterns)

# Function to handle alerts
def handle_alert(alert_message, ip_address, url):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    alert_details = f"{timestamp} - {alert_message} from {ip_address} requesting {url}"
    print(alert_details)
    write_to_alert_log(alert_details)

# Function to write alerts to a log file
def write_to_alert_log(alert_details):
    with open(ALERT_LOG_FILE, 'a') as f:
        f.write(alert_details + '\n')

# Main function to start monitoring the log file
if __name__ == "__main__":
    monitor_log(LOG_FILE, DEFAULT_REGEX)
