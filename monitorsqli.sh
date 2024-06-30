#!/bin/bash

# Define the path to your Apache access log file
ACCESS_LOG="/var/log/apache2/access.log"

# Define the path where you want to save the SQLi alerts
SQLI_ALERTS="/sqli_alerts.log"

# Define the keywords or patterns indicative of SQLi attacks
SQLI_PATTERNS="(union\s+select|select.*\s+from|insert\s+into|drop\s+table|alter\s+table|delete\s+from)"

# Check if the access log file exists
if [ ! -f "$ACCESS_LOG" ]; then
    echo "Access log file not found: $ACCESS_LOG"
    exit 1
fi

# Search for SQLi patterns in the access log and save alerts to a separate file
grep -Ei "$SQLI_PATTERNS" "$ACCESS_LOG" > "$SQLI_ALERTS"

# Count the number of SQLi alerts found
SQLI_COUNT=$(grep -c -Ei "$SQLI_PATTERNS" "$ACCESS_LOG")

# Output the results
echo "SQL Injection Alerts:"
echo "===================="
cat "$SQLI_ALERTS"
echo "Total SQL Injection Alerts: $SQLI_COUNT"

# Optionally, you can add further actions like sending alerts or notifications

exit 0
