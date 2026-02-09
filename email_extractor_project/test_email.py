import imapclient
import email
import socket

# Email server details
IMAP_SERVER = 'imap.yandex.com'
USERNAME = 'snowj1917@yandex.com'
PASSWORD = 'lxvvishpplanixuj'

# Set socket timeout
socket.setdefaulttimeout(30)

# Connect to the server
client = imapclient.IMAPClient(IMAP_SERVER, ssl=True)
client.login(USERNAME, PASSWORD)

# Select folder
client.select_folder('frmt|logs')

# Get all messages
messages = client.search(['ALL'])
print(f"Found {len(messages)} messages\n")

# Fetch first message to see its content
if messages:
    msg_id = messages[-1]  # Get the most recent message
    print(f"Fetching message ID: {msg_id}\n")
    raw_message = client.fetch([msg_id], ['BODY[]'])
    email_message = email.message_from_bytes(raw_message[msg_id][b'BODY[]'])
    
    # Print subject
    print(f"Subject: {email_message.get('subject')}\n")
    
    # Get body
    body = ""
    if email_message.is_multipart():
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    body = payload.decode('utf-8', errors='ignore')
                    break
    else:
        payload = email_message.get_payload(decode=True)
        if payload:
            body = payload.decode('utf-8', errors='ignore')
    
    print("=" * 60)
    print("MESSAGE BODY:")
    print("=" * 60)
    print(body)
    print("=" * 60)

client.logout()
