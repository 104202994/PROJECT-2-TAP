# Email details
recipient="104202994@student.swin.edu.au"
sender="104202994@student.swin.edu.au"
subject="Test Email from Swatch"
body="This is a test email from Swatch."

# Send email using AWS SES via AWS CLI
aws ses send-email \
    --from "$sender" \
    --to "$recipient" \
    --subject "$subject" \
    --text "$body" \
    --region us-east-1
