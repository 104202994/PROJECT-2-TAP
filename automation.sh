#!/bin/bash

chmod +x /path/to/automation.sh

# Define paths to Swatch executable and log files
SWATCH_PATH="/usr/local/bin/swatch"
LOGFILE_PATH="/path/to/logfile.log"

# Define paths to configuration files
EXECUTION_CONF="/path/to/execution/swatch_execution.conf"
INJECTION_CONF="/path/to/injection/swatch_injection.conf"
SESSION_CONF="/path/to/session/swatch_session.conf"
PHISHING_CONF="/path/to/phishing/swatch_phishing.conf"

# Define paths to Python scripts
EXECUTION_PY="/path/to/execution/execution.py"
INJECTION_PY="/path/to/injection/injection.py"
SESSION_PY="/path/to/session/session.py"
PHISHING_PY="/path/to/phishing/phishing.py"

# Define categories for attack types
CATEGORY_EXECUTION="Execution"
CATEGORY_INJECTION="Injection"
CATEGORY_SESSION="Session"
CATEGORY_PHISHING="Phishing"

# Run Python scripts
echo "Running Python script for Execution Attack..."
python3 $EXECUTION_PY &
pid_execution_py=$!

echo "Running Python script for Injection Attack..."
python3 $INJECTION_PY &
pid_injection_py=$!

echo "Running Python script for Session Attack..."
python3 $SESSION_PY &
pid_session_py=$!

echo "Running Python script for Phishing Attack..."
python3 $PHISHING_PY &
pid_phishing_py=$!

# Run Swatch for each configuration file
echo "Running Swatch for Execution Attack..."
$SWATCH_PATH --config-file=$EXECUTION_CONF --input-file=$LOGFILE_PATH --category="$CATEGORY_EXECUTION" &
pid_execution_swatch=$!

echo "Running Swatch for Injection Attack..."
$SWATCH_PATH --config-file=$INJECTION_CONF --input-file=$LOGFILE_PATH --category="$CATEGORY_INJECTION" &
pid_injection_swatch=$!

echo "Running Swatch for Session Attack..."
$SWATCH_PATH --config-file=$SESSION_CONF --input-file=$LOGFILE_PATH --category="$CATEGORY_SESSION" &
pid_session_swatch=$!

echo "Running Swatch for Phishing Attack..."
$SWATCH_PATH --config-file=$PHISHING_CONF --input-file=$LOGFILE_PATH --category="$CATEGORY_PHISHING" &
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
CRON_JOB="0 * * * * /path/to/run_swatch_and_python.sh"

# Check if the cron job already exists
CRON_JOB_EXISTS=$(crontab -l | grep -F "$CRON_JOB")

if [ -z "$CRON_JOB_EXISTS" ]; then
    echo "Adding cron job..."
    (crontab -l ; echo "$CRON_JOB") | crontab -
else
    echo "Cron job already exists."
fi
