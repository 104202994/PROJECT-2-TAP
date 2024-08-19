import subprocess
import requests
import os
import logging
import json
import sys
import re

# Set up logging
logging.basicConfig(filename='/var/log/c2_response.log', level=logging.INFO, format='%(asctime)s %(message)s')

# Email alert configuration
api_key = 'apikey'
endpoint = 'https://api.brevo.com/v3/smtp/email'
email_data = {
    "sender": {"name": "Security Alert", "email": "tapmonitor2024@gmail.com"},
    "to": [{"email": "abhashspko@gmail.com", "name": "Admin"}],
    "subject": "C2 Threat Detected",
    "htmlContent": ""
}
headers = {
    'api-key': api_key,
    'Content-Type': 'application/json'
}

def send_email(subject, body):
    email_data['subject'] = subject
    email_data['htmlContent'] = f"<html><body><h1>{subject}</h1><p>{body}</p></body></html>"
    try:
        response = requests.post(endpoint, headers=headers, json=email_data)
        if response.status_code == 201:
            logging.info("Email sent successfully.")
        else:
            logging.error(f"Failed to send email: {response.status_code} - {response.text}")
    except Exception as e:
        logging.error(f"Exception occurred while sending email: {e}")

def block_ip(ip):
    try:
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        logging.info(f"Blocked IP: {ip}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to block IP {ip}: {e}")

def kill_processes(pid):
    try:
        subprocess.run(["sudo", "kill", "-9", pid], check=True)
        logging.info(f"Killed process with PID: {pid}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to kill process with PID {pid}: {e}")

def delete_malicious_script(script_path):
    try:
        if os.path.exists(script_path):
            os.remove(script_path)
            logging.info(f"Deleted malicious script: {script_path}")
        else:
            logging.info(f"No malicious script found at {script_path}.")
    except Exception as e:
        logging.error(f"Failed to delete script {script_path}: {e}")

def set_dvwa_security_to_impossible():
    try:
        config_file = "/var/www/html/DVWA/config/config.inc.php"
        subprocess.run(["sudo", "sed", "-i", "s/$_DVWA['default_security_level'] = 'low';/$_DVWA['default_security_level'] = 'impossible';/", config_file], check=True)
        logging.info("DVWA security level set to impossible.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to set DVWA security level: {e}")

def handle_c2_threat(details):
    logging.info(f"Handling C2 threat: {details}")
    send_email("C2 Threat Detected", details)
    
    # Extract relevant information from the log entry
    parts = details.split()
    if len(parts) >= 2 and parts[1] == "C2_DETECTION:":
        # Process information is in the square brackets
        process_info = ' '.join(parts[4:])
        # Extract PID (assuming it's the second field in the process info)
        pid = process_info.split()[1] if len(process_info.split()) > 1 else "Unknown"
        
        kill_processes(pid)
        logging.info(f"Attempted to kill process with PID: {pid}")
    
    delete_malicious_script("/var/www/html/DVWA/hackable/uploads/reverse_shell.sh")
    set_dvwa_security_to_impossible()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        handle_c2_threat(' '.join(sys.argv[1:]))
    else:
        logging.error("No C2 threat details provided.")
