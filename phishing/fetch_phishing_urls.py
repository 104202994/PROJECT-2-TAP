import requests

# URL of the OpenPhish feed
OPENPHISH_URL = 'https://openphish.com/feed.txt'

# Output file to store the phishing URLs
OUTPUT_FILE = 'phishing_blacklist.txt'

def fetch_phishing_urls():
    try:
        response = requests.get(OPENPHISH_URL)
        response.raise_for_status()  # Check for HTTP errors

        # Write the URLs to the output file
        with open(OUTPUT_FILE, 'w') as file:
            file.write(response.text)
        
        print(f"Phishing URLs successfully fetched and saved to {OUTPUT_FILE}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch phishing URLs: {e}")

if __name__ == '__main__':
    fetch_phishing_urls()
