#!/bin/bash

# Path to the swatch configuration file
SWATCH_CONFIG=/home/nil/Desktop/Swatch/config/swatchrc

# Path to the log file to monitor
LOG_FILE=/opt/lampp/logs/access_log

# Use tail to follow the log file and pipe it to the Python scripts
tail -f $LOG_FILE | python3 /home/nil/Desktop/Swatch/scripts/detect_bruteforce.py
