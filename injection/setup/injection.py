import re
from datetime import datetime

# User-defined regex pattern and log file path (adjust these as necessary)
DEFAULT_REGEX = r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(\w+) (.*?) HTTP/.*?" \d+ \d+ "([^"]*)" "([^"]*)"'
LOG_FILE = 'injection_user_access.log'
ALERT_LOG_FILE = 'injection_alerts.log'

# Function to parse a log line and extract relevant details
def parse_log_line(line, pattern):
    match = re.match(pattern, line)
    if match:
        ip_address = match.group(1)
        method = match.group(3)
        url = match.group(4)
        query_string = match.group(5)
        return ip_address, method, url, query_string
    return None, None, None, None

# Function to monitor the log file for suspicious activities
def check_logs_for_injection_attacks(log_file, pattern):
    with open(log_file, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                ip_address, method, url, query_string = parse_log_line(line, pattern)
                if ip_address:
                    detect_injection_attacks(ip_address, method, url, query_string)

# Function to detect injection attacks based on parsed log details
def detect_injection_attacks(ip_address, method, url, query_string):
    if detect_command_injection(url, query_string):
        handle_alert("Command Injection detected", ip_address, method, url, query_string)
    elif detect_ldap_injection(query_string):
        handle_alert("LDAP Injection detected", ip_address, method, url, query_string)
    elif detect_nosql_injection(query_string):
        handle_alert("NoSQL Injection detected", ip_address, method, url, query_string)
    elif detect_ssrf(url):
        handle_alert("SSRF detected", ip_address, method, url, query_string)

# Function to detect Command Injection attempts
def detect_command_injection(url, query_string):
    return any(keyword in url or keyword in query_string for keyword in [';', '&&', '|', '`'])

# Function to detect LDAP Injection attempts
def detect_ldap_injection(query_string):
    return any(keyword in query_string for keyword in ['(|', '(&', '*)'])

# Function to detect NoSQL Injection attempts
def detect_nosql_injection(query_string):
    return any(keyword in query_string for keyword in ['{"', '}', '$ne', '$eq', '$gt', '$lt'])

# Function to detect SSRF attempts
def detect_ssrf(url):
    return '127.0.0.1' in url or 'localhost' in url or '169.254.' in url

# Function to handle alerts
def handle_alert(alert_message, ip_address, method, url, query_string):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    alert_details = f"{timestamp} - {alert_message} from {ip_address} using {method} on {url} with query {query_string}"
    print(alert_details)
    write_to_alert_log(alert_details)

# Function to write alerts to a log file
def write_to_alert_log(alert_details):
    with open(ALERT_LOG_FILE, 'a') as log_file:
        log_file.write(alert_details + '\n')

# Main function to start monitoring the log file
if __name__ == "__main__":
    check_logs_for_injection_attacks(LOG_FILE, DEFAULT_REGEX)
