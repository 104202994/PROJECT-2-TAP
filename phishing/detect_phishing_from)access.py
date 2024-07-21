import re

# Paths to the log file and blacklist file
LOG_FILE = 'user_access.log'
BLACKLIST_FILE = 'phishing_blacklist.txt'
LOG_OUTPUT_FILE = 'phishing_alerts.log'

def load_blacklist():
    """Load the blacklist URLs from the file."""
    with open(BLACKLIST_FILE, 'r') as file:
        return set(line.strip() for line in file)

def check_logs_for_phishing(log_file, blacklist):
    """Check the log file for blacklisted URLs."""
    phishing_detected = False
    with open(log_file, 'r') as file:
        for line in file:
            urls = re.findall(r'\"(http[^\"]+)\"', line)
            for url in urls:
                if any(blacklisted_url in url for blacklisted_url in blacklist):
                    phishing_detected = True
                    log_phishing_attempt(url)
                    
    if phishing_detected:
        print(f"Phishing attack detected. Check {LOG_OUTPUT_FILE} for details.")
    else:
        print("No phishing attacks detected.")

def log_phishing_attempt(phishing_url):
    """Log the phishing attempt details to the log file."""
    with open(LOG_OUTPUT_FILE, 'a') as log_file:
        log_message = f"Phishing attack detected: {phishing_url}"
        log_file.write(log_message + '\n')

if __name__ == '__main__':
    blacklist = load_blacklist()
    check_logs_for_phishing(LOG_FILE, blacklist)
