# Security Monitoring Script Explanation

## Overview

This report provides an overview of a suite of Python scripts designed to detect and respond to various security threats by monitoring Apache access logs. Each script focuses on a specific type of attack, including Brute Force, Directory Traversal, Denial of Service (DoS), and File Inclusion attacks. The scripts perform real-time monitoring, detect malicious activities, and take appropriate actions such as blocking IP addresses and sending alerts.

## 1. `detectBruteForce.py`

### Type of Attack: Brute Force Attack

A Brute Force Attack involves an attacker trying many different passwords or credentials to gain unauthorized access to a system. In the context of web applications, this often means attempting numerous login attempts to crack user accounts.

### Functions and Actions:

- **`parse_log_line(line)`**
  - **Purpose**: Extracts the IP address from a log line if it matches the pattern of a brute force attempt.
  - **Scenario**: Logs showing repeated login attempts from a single IP address.

- **`block_ip_address(ip_address)`**
  - **Purpose**: Blocks the IP address using `iptables` if a brute force attack is detected.
  - **Action**: Executes a system command to drop packets from the offending IP, preventing further access.

- **`is_brute_force(ip_address, current_time)`**
  - **Purpose**: Determines if the IP address has made too many attempts within a specified timeframe.
  - **Scenario**: Checks if the number of login attempts exceeds a threshold, indicating a potential brute force attack.

- **`monitor_log_file()`**
  - **Purpose**: Continuously monitors the access log file for new entries and processes each line.
  - **Action**: Detects and reacts to brute force attacks by blocking IP addresses and sending Slack notifications.

## 2. `detectDirectoryTraversal.py`

### Type of Attack: Directory Traversal Attack

Directory Traversal attacks exploit vulnerabilities to access files and directories outside the intended scope of a web application. Attackers use specially crafted input to navigate to unauthorized files.

### Functions and Actions:

- **`parse_log_line(line)`**
  - **Purpose**: Identifies IP addresses from log lines that contain directory traversal patterns.
  - **Scenario**: Detects suspicious patterns like `../` or encoded directory traversal sequences.

- **`block_ip_address(ip_address)`**
  - **Purpose**: Blocks the IP address using `iptables` upon detecting a directory traversal attempt.
  - **Action**: Prevents further access from the malicious IP.

- **`monitor_log_file()`**
  - **Purpose**: Continuously checks the access log file for entries indicating directory traversal attempts.
  - **Action**: Detects and reacts to directory traversal attacks by blocking IP addresses and sending alerts.

## 3. `detectDos.py`

### Type of Attack: Denial of Service (DoS) Attack

A Denial of Service (DoS) attack aims to make a service unavailable by overwhelming it with traffic or requests, thereby disrupting legitimate access.

### Functions and Actions:

- **`parse_log_line(line)`**
  - **Purpose**: Extracts IP addresses and requested endpoints from log lines.
  - **Scenario**: Identifies requests that may indicate a potential DoS attack.

- **`block_ip_address(ip_address)`**
  - **Purpose**: Blocks the IP address if a DoS attack is detected.
  - **Action**: Uses `iptables` to drop packets from the offending IP address.

- **`check_for_dos(ip_address, endpoint)`**
  - **Purpose**: Checks if the request frequency for a specific endpoint from an IP address exceeds the threshold.
  - **Scenario**: Monitors request counts and blocks IP addresses that exceed the allowed request limit.

- **`monitor_log_file()`**
  - **Purpose**: Continuously monitors the log file for signs of a DoS attack by tracking request patterns.
  - **Action**: Detects and responds to potential DoS attacks by blocking IP addresses and sending alerts.

## 4. `detectFileInclusion.py`

### Type of Attack: File Inclusion Attack

File Inclusion attacks allow attackers to include files on a server, potentially leading to unauthorized access or code execution. These attacks are categorized into Remote File Inclusion (RFI) and Local File Inclusion (LFI).

### Functions and Actions:

- **`detect_rfi(line)`**
  - **Purpose**: Detects attempts to include files from remote locations.
  - **Scenario**: Identifies URLs pointing to external resources in log lines.
  - **Action**: Updates the `php.ini` configuration to disable remote file inclusion and restarts the Apache server.

- **`detect_lfi(line)`**
  - **Purpose**: Detects attempts to include local files.
  - **Scenario**: Looks for file paths in the log that attempt to navigate outside the allowed directories.
  - **Action**: Blocks the IP address if the file paths are not among the allowed ones.

- **`block_ip_address(ip_address, attack_type)`**
  - **Purpose**: Blocks the IP address using `iptables` for detected file inclusion attempts.
  - **Action**: Prevents further access from the malicious IP.

- **`update_php_ini()`**
  - **Purpose**: Disables `allow_url_include` in the `php.ini` configuration file to prevent remote file inclusions.
  - **Action**: Edits configuration and restarts Apache to apply changes.

- **`restart_apache()`**
  - **Purpose**: Restarts the Apache server to apply configuration changes.
  - **Action**: Ensures the updated configuration takes effect.

- **`monitor_log_file()`**
  - **Purpose**: Continuously monitors the log file for file inclusion attempts.
  - **Action**: Detects and responds to both RFI and LFI attacks by blocking IP addresses and updating server configurations.

## 5. `detectAttacks.py`

### Purpose: Coordinating Script Execution

This script is responsible for managing and running the individual detection scripts concurrently. It ensures that each detection script operates in parallel, allowing real-time monitoring of various types of attacks.

### Functions and Actions:

- **`run_script(script_name)`**
  - **Purpose**: Executes a given script and prints its real-time output and errors.
  - **Action**: Uses `subprocess.Popen` to run detection scripts and monitor their output.

- **`__main__` Block**
  - **Purpose**: Runs all detection scripts concurrently using `ThreadPoolExecutor`.
  - **Action**: Manages parallel execution, handles script results, and catches errors.

## Conclusion

The provided scripts form a comprehensive security monitoring solution that detects various web application attacks by analyzing Apache access logs. They perform real-time monitoring, take defensive actions such as blocking IP addresses, and provide notifications to administrators. Each script is tailored to address specific attack vectors, ensuring robust protection against unauthorized access and service disruptions.
