import re
import os

# Paths to the email source file, blacklist file, and log file
EMAIL_SOURCE_FILE = 'email_source.html'
BLACKLIST_FILE = 'phishing_blacklist.txt'
LOG_FILE = 'phishing_alerts.log'

def load_blacklist():
    """Load the blacklist URLs from the file."""
    with open(BLACKLIST_FILE, 'r') as file:
        return set(line.strip() for line in file)

def check_for_phishing(email_source, blacklist):
    """Check the email source for URLs in the blacklist and log any matches."""
    phishing_detected = False

    with open(email_source, 'r') as file:
        email_content = file.read()

    # Find all href attributes
    href_pattern = re.compile(r'href="([^"]+)"')
    urls = href_pattern.findall(email_content)

    for url in urls:
        if any(blacklisted_url in url for blacklisted_url in blacklist):
            phishing_detected = True
            log_phishing_attempt(url)
    
    if phishing_detected:
        print(f"Phishing attack detected. Check {LOG_FILE} for details.")
    else:
        print("No phishing attacks detected.")

def log_phishing_attempt(phishing_url):
    """Log the phishing attempt details to the log file."""
    with open(LOG_FILE, 'a') as log_file:
        log_message = f"Phishing attack detected: {phishing_url}"
        log_file.write(log_message + '\n')

if __name__ == '__main__':
    # Create the log file if it doesn't exist
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, 'w').close()

    blacklist = load_blacklist()
    check_for_phishing(EMAIL_SOURCE_FILE, blacklist)
