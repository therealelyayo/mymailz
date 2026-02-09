# MyMailz - Email Query Interface

A web-based email management application powered by Nylas API. Query and manage emails with an intuitive interface, with support for dynamic grant ID management.

## Features

- 📧 **Email Parsing**: Parse and display emails using Nylas API
- 🔍 **Advanced Query**: Filter emails by subject, sender, and limit results
- 🔑 **Grant ID Management**: Easily change and update grant IDs through the UI
- 💬 **Email Details**: View full email content including headers and body
- 🎨 **Modern UI**: Clean, responsive interface with real-time updates
- ⚡ **Fast & Efficient**: Built with Flask and modern web technologies

## Prerequisites

- Python 3.7 or higher
- Nylas API account and credentials
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/therealelyayo/mymailz.git
cd mymailz
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
```

4. Edit `.env` file with your Nylas credentials:
```env
NYLAS_API_KEY=your_api_key_here
NYLAS_API_URI=https://api.us.nylas.com
NYLAS_GRANT_ID=your_grant_id_here
DEBUG=False  # Set to True only for development
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Update the Grant ID in the UI if needed

4. Query emails using the search interface

## API Endpoints

### Get Grant ID
```
GET /api/grant-id
```

### Update Grant ID
```
POST /api/grant-id
Content-Type: application/json

{
  "grant_id": "new_grant_id"
}
```

### Query Emails
```
GET /api/emails?limit=20&subject=test&from=sender@example.com
```

Parameters:
- `limit`: Number of emails to fetch (default: 20)
- `subject`: Filter by email subject (optional)
- `from`: Filter by sender email (optional)

### Get Email Detail
```
GET /api/email/<email_id>
```

## Project Structure

```
mymailz/
├── app.py                 # Flask application and API endpoints
├── templates/
│   └── index.html        # Web UI interface
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Security Notes

- Never commit your `.env` file with real credentials
- Keep your Nylas API key secure
- Use environment variables for all sensitive data
- The `.env` file is already in `.gitignore`

## Technologies Used

- **Backend**: Python Flask
- **Email API**: Nylas SDK
- **Frontend**: HTML, CSS, JavaScript
- **Configuration**: python-dotenv

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
- Check Nylas API documentation: https://developer.nylas.com/
- Open an issue on GitHub

## Author

Created by @therealelyayo