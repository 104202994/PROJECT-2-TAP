import re  # Import regular expression library
from collections import defaultdict  # Import defaultdict for nested dictionaries
from datetime import datetime, timedelta  # Import datetime objects for timestamp manipulation

def parse_log(file_path):
    # Regular expression pattern to extract IP address, timestamp, HTTP method, and URL
    pattern = r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) .* \[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}) \+\d{4}\] "(GET|POST|PUT|DELETE) (\S+) HTTP/\d\.\d"'

    # Dictionary to store counts of IP addresses accessing each URL per minute
    ip_url_counts_per_minute = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    # Open and read the log file
    with open(file_path, 'r') as file:
        for line in file:
            # Use regex to find IP address, timestamp, HTTP method, and URL in each line
            match = re.search(pattern, line)
            if match:
                ip_address = match.group(1)
                timestamp_str = match.group(2)
                http_method = match.group(3)
                url = match.group(4)

                # Parse timestamp string into datetime object
                timestamp = datetime.strptime(timestamp_str, '%d/%b/%Y:%H:%M:%S')

                # Round down the timestamp to the nearest minute
                minute_timestamp = timestamp.replace(second=0, microsecond=0)

                # Increment count for this IP, URL, and minute timestamp
                ip_url_counts_per_minute[ip_address][url][minute_timestamp] += 1

    return ip_url_counts_per_minute

def check_dos_attack(counts_per_minute, threshold=20):
    # List to store details of potential attacks
    potential_attacks = []

    for ip_address, url_counts in counts_per_minute.items():
        for url, minute_counts in url_counts.items():
            for minute_timestamp, count in minute_counts.items():
                if count > threshold:
                    next_minute_timestamp = minute_timestamp + timedelta(minutes=1)
                    attack_timeframe = f"{minute_timestamp.strftime('%Y-%m-%d %H:%M')} to {next_minute_timestamp.strftime('%Y-%m-%d %H:%M')}"
                    potential_attacks.append(f"{ip_address} tried to access '{url}' {count} times within the timeframe of {attack_timeframe}")

    if potential_attacks:
        print("-------------------------------------------------Alert! Potential DoS attack detected-------------------------------------------------")
        for attack_details in potential_attacks:
            print(attack_details)
    else:
        print("No attack detected.")

# Example usage:
if __name__ == "__main__":
    log_file = "/opt/lampp/logs/access_log"  #log file path
    counts_per_minute = parse_log(log_file)
    
    # Print potential DoS attacks if any IP accesses a URL more than 20 times per minute
    check_dos_attack(counts_per_minute, threshold=20)
