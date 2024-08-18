#!/bin/bash

chmod +x "$(dirname "$0")/automation.sh"

# Read the log file path from the temporary file created by the Python script
TEMP_FILE_PATH="/tmp/log_file_path.txt"
if [ -f "$TEMP_FILE_PATH" ]; then
    LOGFILE_PATH=$(cat "$TEMP_FILE_PATH")
    echo "Log file path set to $LOGFILE_PATH"
else
    echo "Error: Log file path not set. Please run the Python script first."
    exit 1
fi

# Define paths to Swatch executable
SWATCH_PATH="/usr/local/bin/swatch"

# Define paths to configuration files
EXECUTION_CONF="/execution/setup/swatch_execution.conf"
INJECTION_CONF="/injection/setup/swatch_injection.conf"
SESSION_CONF="/session/setup/swatch_session.conf"
PHISHING_CONF="/phishing/setup/swatch_phishing.conf"

# Define paths to Python scripts
EXECUTION_PY="/execution/setup/execution.py"
INJECTION_PY="/injection/setup/injection.py"
SESSION_PY="/session/setup/session.py"
PHISHING_PY="/phishing/setup/phishing.py"

# Define categories for attack types
CATEGORY_EXECUTION="Execution"
CATEGORY_INJECTION="Injection"
CATEGORY_SESSION="Session"
CATEGORY_PHISHING="Phishing"

# Run Python scripts
echo "Running Python script for Execution Attack..."
python3 "$SCRIPT_DIR/$EXECUTION_PY" &
pid_execution_py=$!

echo "Running Python script for Injection Attack..."
python3 "$SCRIPT_DIR/$INJECTION_PY" &
pid_injection_py=$!

echo "Running Python script for Session Attack..."
python3 "$SCRIPT_DIR/$SESSION_PY" &
pid_session_py=$!

echo "Running Python script for Phishing Attack..."
python3 "$SCRIPT_DIR/$PHISHING_PY" &
pid_phishing_py=$!

# Run Swatch for each configuration file
echo "Running Swatch for Execution Attack..."
$SWATCH_PATH --config-file="$SCRIPT_DIR/$EXECUTION_CONF" --input-file="$LOGFILE_PATH" --category="$CATEGORY_EXECUTION" &
pid_execution_swatch=$!

echo "Running Swatch for Injection Attack..."
$SWATCH_PATH --config-file="$SCRIPT_DIR/$INJECTION_CONF" --input-file="$LOGFILE_PATH" --category="$CATEGORY_INJECTION" &
pid_injection_swatch=$!

echo "Running Swatch for Session Attack..."
$SWATCH_PATH --config-file="$SCRIPT_DIR/$SESSION_CONF" --input-file="$LOGFILE_PATH" --category="$CATEGORY_SESSION" &
pid_session_swatch=$!

echo "Running Swatch for Phishing Attack..."
$SWATCH_PATH --config-file="$SCRIPT_DIR/$PHISHING_CONF" --input-file="$LOGFILE_PATH" --category="$CATEGORY_PHISHING" &
pid_phishing_swatch=$!

# Wait for all background processes to complete
wait $pid_execution_py
wait $pid_injection_py
wait $pid_session_py
wait $pid_phishing_py

wait $pid_execution_swatch
wait $pid_injection_swatch
wait $pid_session_swatch
wait $pid_phishing_swatch

echo "Python scripts and Swatch monitoring completed for all attack types."

# Add cron job if it does not already exist
CRON_JOB="0 * * * * $SCRIPT_DIR/automation.sh"

# Check if the cron job already exists
CRON_JOB_EXISTS=$(crontab -l | grep -F "$CRON_JOB")

if [ -z "$CRON_JOB_EXISTS" ]; then
    echo "Adding cron job..."
    (crontab -l ; echo "$CRON_JOB") | crontab -
else
    echo "Cron job already exists."
fi
