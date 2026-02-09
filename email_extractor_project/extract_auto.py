import imapclient
import email
import re
import socket
from email.header import decode_header
import sys

# Email server details
IMAP_SERVER = 'imap.yandex.com'
USERNAME = 'weder@yandex.com'
PASSWORD = 'lxvviereshpplanixuj'

# Set socket timeout to prevent hanging
socket.setdefaulttimeout(30)

# Connect to the server
client = imapclient.IMAPClient(IMAP_SERVER, ssl=True)
client.login(USERNAME, PASSWORD)

# Use command line arguments or defaults
folder = sys.argv[1] if len(sys.argv) > 1 else 'frmt|logs'
max_messages = int(sys.argv[2]) if len(sys.argv) > 2 else 500

print(f"Selected folder: {folder}")
client.select_folder(folder)

# Search for all messages
all_messages = client.search(['ALL'])
messages = all_messages[-max_messages:] if len(all_messages) > max_messages else all_messages
print(f"Found {len(all_messages)} messages, processing the most recent {len(messages)}...\n")

# Prepare a list to hold extracted data
extracted_data = []

# Open files for appending
username_file = open('usernames.txt', 'w')
password_file = open('passwords.txt', 'w')

try:
    for i, msg_id in enumerate(messages, 1):
        try:
            print(f"[{i}/{len(messages)}] Processing message {msg_id}...", end=' ')
            # Fetch the email
            raw_message = client.fetch([msg_id], ['BODY[]'])
            email_message = email.message_from_bytes(raw_message[msg_id][b'BODY[]'])
            
            # Get the body (assuming plain text; handle multipart if needed)
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
            
            # Use regex to extract fields - matches format like: - *Username*: value
            username_match = re.search(r'-\s*\*Username\*:\s*([^\n]+)', body, re.IGNORECASE)
            password_match = re.search(r'-\s*\*Password\*:\s*([^\n]+)', body, re.IGNORECASE)
            confpass_match = re.search(r'-\s*\*Confpass\*:\s*([^\n]+)', body, re.IGNORECASE)
            
            # If all fields are found, add to data and save immediately
            if username_match and password_match and confpass_match:
                username = username_match.group(1).strip()
                password = password_match.group(1).strip()
                confpass = confpass_match.group(1).strip()
                
                extracted_data.append({
                    'username': username,
                    'password': password,
                    'confpass': confpass
                })
                
                # Write immediately to files
                username_file.write(f"{username}\n")
                username_file.flush()
                password_file.write(f"{password}\n")
                password_file.flush()
                
                print("✓")
            else:
                print("⊘")
        except Exception as e:
            print(f"✗ Error: {e}")
            continue
finally:
    # Close files
    username_file.close()
    password_file.close()

# Logout
client.logout()

print(f"\n✅ Extracted {len(extracted_data)} entries:")
print(f"  - Usernames saved to usernames.txt")
print(f"  - Passwords saved to passwords.txt")
