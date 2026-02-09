import imapclient
import email
import re
import socket
from email.header import decode_header
 Email server details
IMAP_SERVER = 'imap.yandex.com'
USERNAME = 'weder@yandex.com'
PASSWORD = 'lxvviereshpplanixuj'
 Use an app password, not your main password

# Set socket timeout to prevent hanging
socket.setdefaulttimeout(30)

# Connect to the server
client = imapclient.IMAPClient(IMAP_SERVER, ssl=True)
client.login(USERNAME, PASSWORD)

# List all folders
folders = client.list_folders()
print("\n=== Available Folders ===")
for i, (flags, delimiter, name) in enumerate(folders, 1):
    print(f"{i}. {name}")

# Ask user to choose a folder
folder_choice = input("\nEnter folder number (or press Enter for INBOX): ").strip()
if folder_choice.isdigit() and 1 <= int(folder_choice) <= len(folders):
    selected_folder = folders[int(folder_choice) - 1][2]
else:
    selected_folder = 'INBOX'

print(f"\nSelected folder: {selected_folder}")

# Select the folder
client.select_folder(selected_folder)

# Ask for search query
print("\nSearch options:")
print("1. ALL - All messages")
print("2. UNSEEN - Unread messages")
print("3. SEEN - Read messages")
print("4. SUBJECT <text> - Messages with specific subject")
print("5. FROM <email> - Messages from specific sender")
print("6. SINCE <date> - Messages since date (format: DD-Mon-YYYY, e.g., 01-Jan-2026)")

query_input = input("\nEnter search query (or press Enter for 'ALL'): ").strip().upper()
if not query_input:
    search_criteria = ['ALL']
else:
    # Parse the input into search criteria
    search_criteria = query_input.split()

print(f"\nSearching with criteria: {search_criteria}")

# Search for messages
all_messages = client.search(search_criteria)
MAX_MESSAGES = 500  # Limit to avoid processing too many
messages = all_messages[-MAX_MESSAGES:] if len(all_messages) > MAX_MESSAGES else all_messages
print(f"Found {len(all_messages)} messages, processing the most recent {len(messages)}...")

# Prepare a list to hold extracted data
extracted_data = []

# Open files for appending
username_file = open('usernames.txt', 'w')
password_file = open('passwords.txt', 'w')

try:
    for msg_id in messages:
        try:
            print(f"Processing message {msg_id}...")
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
                
                print(f"  ✓ Extracted data from message {msg_id}")
        except Exception as e:
            print(f"  ✗ Error processing message {msg_id}: {e}")
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
