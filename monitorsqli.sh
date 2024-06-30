#!/bin/bash

# Define the path to your Apache access log file
ACCESS_LOG="/var/log/apache2/access.log"

# Define the path where you want to save the SQLi alerts
SQLI_ALERTS="/sqli_alerts.log"

# Define the keywords or patterns indicative of SQLi attacks with more flexibility for whitespace
SQLI_PATTERNS="(union\s+select|select\s+.*\s+from|insert\s+into|drop\s+table|alter\s+table|delete\s+from)"

# Check if the access log file exists
if [ ! -f "$ACCESS_LOG" ]; then
    echo "Access log file not found: $ACCESS_LOG"
    exit 1
fi

# Search for SQLi patterns in the access log with options for encoding and case-insensitivity
grep -E --color=never -i "$SQLI_PATTERNS" "$ACCESS_LOG" > "$SQLI_ALERTS"

# Count the number of SQLi alerts found using grep -c
SQLI_COUNT=$(grep -c -E --color=never -i "$SQLI_PATTERNS" "$ACCESS_LOG")

# Output the results
echo "SQL Injection Alerts:"
echo "===================="
cat "$SQLI_ALERTS"
echo "Total SQL Injection Alerts: $SQLI_COUNT"

# Optionally, you can add further actions like sending alerts or notifications

exit 0
