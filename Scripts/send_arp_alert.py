import sys
import subprocess
import requests
import json
import time

# Define your API key and endpoint
api_key = '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'
endpoint = 'https://api.brevo.com/v3/smtp/email'

# Define the email details
email_data = {
    "sender": {"name": "Security Alert", "email": "tapmonitor2024@gmail.com"},
    "to": [{"email": "abhashspko@gmail.com", "name": "Anonymous"}],  # Replace with your email
    "subject": "Security Alert",
    "htmlContent": "<html><body><h1>Alert</h1><p>This is a security alert notification.</p></body></html>"
}

# Set the headers for the email API request
headers = {
    'api-key': api_key,
    'Content-Type': 'application/json'
}

def send_email(subject, content):
    email_data['subject'] = subject
    email_data['htmlContent'] = f"<html><body><h1>{subject}</h1><p>{content}</p></body></html>"
    
    try:
        print("Sending email...")
        response = requests.post(endpoint, headers=headers, data=json.dumps(email_data))
        print(f"Response status code: {response.status_code}")
        if response.status_code == 201:
            print("Email sent successfully!")
        else:
            print(f"Failed to send email: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Exception occurred while sending email: {e}")

def block_ip(ip):
    try:
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        print(f"Blocked IP: {ip}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to block IP {ip}: {e}")

def unblock_ip(ip):
    try:
        subprocess.run(["sudo", "iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        print(f"Unblocked IP: {ip}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to unblock IP {ip}: {e}")

def reset_arp_tables():
    try:
        subprocess.run(["sudo", "ip", "neigh", "flush", "all"], check=True)
        print("ARP tables flushed.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to reset ARP tables: {e}")

def disable_enable_interface(interface):
    try:
        subprocess.run(["sudo", "ifconfig", interface, "down"], check=True)
        print(f"Interface {interface} down.")
        time.sleep(5)
        subprocess.run(["sudo", "ifconfig", interface, "up"], check=True)
        print(f"Interface {interface} up.")
        time.sleep(5)  # Added delay to allow network recovery
    except subprocess.CalledProcessError as e:
        print(f"Failed to disable/enable interface {interface}: {e}")

def get_gateway_ip():
    try:
        result = subprocess.run(["ip", "route"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if "default" in line:
                return line.split()[2]
    except Exception as e:
        print(f"Error getting gateway IP: {e}")
    return None

def get_local_mac(interface):
    try:
        result = subprocess.run(["cat", f"/sys/class/net/{interface}/address"], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"Error getting local MAC address: {e}")
    return None

def broadcast_correct_arp(interface, duration=60, interval=5):
    gateway_ip = get_gateway_ip()
    local_mac = get_local_mac(interface)

    if gateway_ip and local_mac:
        start_time = time.time()
        while time.time() - start_time < duration:
            try:
                subprocess.run(["sudo", "arping", "-U", "-c", "3", "-I", interface, "-s", local_mac, gateway_ip], check=True)
                print(f"Broadcasted correct ARP info for IP {gateway_ip} with MAC {local_mac}.")
                time.sleep(interval)
            except subprocess.CalledProcessError as e:
                print(f"Failed to broadcast correct ARP info: {e}")
    else:
        print("Failed to determine gateway IP or local MAC address.")

def handle_ip(ip):
    if ip != '-' and ip.count('.') == 3:  # Basic check to ensure it's a valid IP
        print(f"Handling IP: {ip}")
        
        # Send an email alert
        send_email("ARP Poisoning Detected", f"ARP poisoning detected from IP: {ip}")

        # Block the malicious IP
        block_ip(ip)

        # Reset ARP tables
        reset_arp_tables()

        # Temporarily disable and re-enable the interface
        disable_enable_interface("enp0s1")

        # Dynamically broadcast correct ARP information for 1 minute
        broadcast_correct_arp("enp0s1", duration=60, interval=5)

        # Unblock the IP after 1 minute
        time.sleep(60)
        unblock_ip(ip)
    else:
        print("Invalid IP address detected. Skipping blocking.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python send_arp_alert.py <log_line>")
        sys.exit(1)

    log_line = ' '.join(sys.argv[1:])
    print(f"Log line: {log_line}")

    try:
        parts = log_line.split(' ')
        ip_index = parts.index("ARP_POISON") + 1
        ip = parts[ip_index]
    except ValueError as e:
        print(f"Error parsing log line: {e}")
        sys.exit(1)

    handle_ip(ip)
