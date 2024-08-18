import subprocess
import logging

# Set up logging
logging.basicConfig(filename='/var/log/c2_monitor.log', level=logging.INFO, format='%(asctime)s %(message)s')

# Function to monitor network activity for potential C2
def monitor_network():
    try:
        result = subprocess.run(["netstat", "-tulnp"], capture_output=True, text=True)
        suspicious_connections = [line for line in result.stdout.splitlines() if 'ESTABLISHED' in line and 'safe_processes' not in line]
        if suspicious_connections:
            logging.info(f"C2_CONNECTION detected: {suspicious_connections}")
    except Exception as e:
        logging.error(f"Error monitoring network: {e}")

# Function to monitor for suspicious processes
def monitor_processes():
    try:
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
        suspicious_processes = [line for line in result.stdout.splitlines() if "bash -i" in line or "nc" in line and 'grep' not in line]
        if suspicious_processes:
            logging.info(f"C2_DETECTION: Suspicious process detected: {suspicious_processes}")
    except Exception as e:
        logging.error(f"Error monitoring processes: {e}")

if __name__ == "__main__":
    # Monitor for C2 activity
    monitor_network()
    monitor_processes()
