#!/bin/bash

# Email details
recipient="104202994@student.swin.edu.au"
sender="104202994@student.swin.edu.au"
subject="Test Email from Swatch"
body="This is a test email from Swatch."

# Set AWS environment variables
export AWS_CONFIG_FILE=/home/sparsh/.aws/config
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key

# Send email using Amazon SES via AWS CLI
aws ses send-email \
    --from "$sender" \
    --to "$recipient" \
    --subject "$subject" \
    --text "$body" \
    --region us-east-1


