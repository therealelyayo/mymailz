from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from nylas import Client
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize Nylas client
nylas = Client(
    api_key=os.getenv('NYLAS_API_KEY'),
    api_uri=os.getenv('NYLAS_API_URI', 'https://api.us.nylas.com')
)

# Store current grant_id in app config (thread-safe)
app.config['CURRENT_GRANT_ID'] = os.getenv('NYLAS_GRANT_ID', '')

@app.route('/')
def index():
    """Render the main web UI"""
    return render_template('index.html', grant_id=app.config['CURRENT_GRANT_ID'])

@app.route('/api/grant-id', methods=['GET', 'POST'])
def manage_grant_id():
    """Get or update the grant ID"""
    if request.method == 'POST':
        data = request.get_json()
        new_grant_id = data.get('grant_id', '')
        if new_grant_id:
            app.config['CURRENT_GRANT_ID'] = new_grant_id
            return jsonify({
                'success': True,
                'grant_id': app.config['CURRENT_GRANT_ID'],
                'message': 'Grant ID updated successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Grant ID cannot be empty'
            }), 400
    
    return jsonify({'grant_id': app.config['CURRENT_GRANT_ID']})

@app.route('/api/emails', methods=['GET'])
def get_emails():
    """Query emails using Nylas API"""
    if not app.config['CURRENT_GRANT_ID']:
        return jsonify({
            'success': False,
            'message': 'Grant ID not set. Please configure it first.'
        }), 400
    
    try:
        # Get query parameters
        limit = request.args.get('limit', 20, type=int)
        subject = request.args.get('subject', '')
        from_email = request.args.get('from', '')
        
        # Build query parameters
        query_params = {
            'limit': limit
        }
        
        if subject:
            query_params['subject'] = subject
        if from_email:
            query_params['from'] = from_email
        
        # Fetch messages using Nylas API
        messages, _, _ = nylas.messages.list(
            identifier=app.config['CURRENT_GRANT_ID'],
            query_params=query_params
        )
        
        # Parse and format email data
        emails = []
        for message in messages:
            email_data = {
                'id': message.id,
                'subject': message.subject or '(No Subject)',
                'from': [],
                'to': [],
                'date': message.date,
                'snippet': message.snippet or '',
                'body': message.body or '',
                'unread': message.unread if hasattr(message, 'unread') else False
            }
            
            # Parse from addresses
            if message.from_:
                for sender in message.from_:
                    email_data['from'].append({
                        'name': sender.name or '',
                        'email': sender.email or ''
                    })
            
            # Parse to addresses
            if message.to:
                for recipient in message.to:
                    email_data['to'].append({
                        'name': recipient.name or '',
                        'email': recipient.email or ''
                    })
            
            # Convert timestamp to readable format
            if email_data['date']:
                email_data['date_formatted'] = datetime.fromtimestamp(
                    email_data['date']
                ).strftime('%Y-%m-%d %H:%M:%S')
            else:
                email_data['date_formatted'] = 'Unknown'
            
            emails.append(email_data)
        
        return jsonify({
            'success': True,
            'count': len(emails),
            'emails': emails
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching emails: {str(e)}'
        }), 500

@app.route('/api/email/<email_id>', methods=['GET'])
def get_email_detail(email_id):
    """Get detailed information about a specific email"""
    if not app.config['CURRENT_GRANT_ID']:
        return jsonify({
            'success': False,
            'message': 'Grant ID not set. Please configure it first.'
        }), 400
    
    try:
        # Fetch specific message
        message = nylas.messages.find(
            identifier=app.config['CURRENT_GRANT_ID'],
            message_id=email_id
        )
        
        email_data = {
            'id': message.id,
            'subject': message.subject or '(No Subject)',
            'from': [],
            'to': [],
            'cc': [],
            'bcc': [],
            'date': message.date,
            'body': message.body or '',
            'unread': message.unread if hasattr(message, 'unread') else False,
            'starred': message.starred if hasattr(message, 'starred') else False,
        }
        
        # Parse from addresses
        if message.from_:
            for sender in message.from_:
                email_data['from'].append({
                    'name': sender.name or '',
                    'email': sender.email or ''
                })
        
        # Parse to addresses
        if message.to:
            for recipient in message.to:
                email_data['to'].append({
                    'name': recipient.name or '',
                    'email': recipient.email or ''
                })
        
        # Parse cc addresses
        if hasattr(message, 'cc') and message.cc:
            for recipient in message.cc:
                email_data['cc'].append({
                    'name': recipient.name or '',
                    'email': recipient.email or ''
                })
        
        # Parse bcc addresses
        if hasattr(message, 'bcc') and message.bcc:
            for recipient in message.bcc:
                email_data['bcc'].append({
                    'name': recipient.name or '',
                    'email': recipient.email or ''
                })
        
        # Convert timestamp to readable format
        if email_data['date']:
            email_data['date_formatted'] = datetime.fromtimestamp(
                email_data['date']
            ).strftime('%Y-%m-%d %H:%M:%S')
        else:
            email_data['date_formatted'] = 'Unknown'
        
        return jsonify({
            'success': True,
            'email': email_data
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching email: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
