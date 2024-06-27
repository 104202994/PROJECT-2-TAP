#!/bin/bash

# Path to the flag file for triggering page reload or action
FLAG_FILE="/var/www/html/dvwa/config/reload_flag.txt"

# Create/update the flag file
echo "XSS attack detected" > $FLAG_FILE
