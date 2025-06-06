# Slack to Google Sheets Integration

A Flask application that captures Slack messages and logs them to Google Sheets.

## Features

- ✅ Slack Events API integration
- ✅ Google Sheets API integration
- ✅ Real-time message logging
- ✅ Slack channel summaries

## Setup

### 1. Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file:

```env
SLACK_WEBHOOK_URL=your_webhook_url
SLACK_SIGNING_SECRET=your_signing_secret
SLACK_BOT_TOKEN=your_bot_token
GOOGLE_CREDENTIALS_FILE=credentials.json
GOOGLE_SHEET_ID=your_sheet_id
```

### 3. Google Sheets Setup

1. Create a Google Cloud project
2. Enable Google Sheets API
3. Create a service account and download JSON credentials
4. Save credentials as `credentials.json`
5. Share your Google Sheet with the service account email

## Running the Application

### Start the Flask App

```bash
# Activate virtual environment
source venv/bin/activate

# Run the app
python src/app.py
```

### Run Tests

```bash
# Test Slack API connection
python src/test_slack.py

# Test Google Sheets API connection
python src/test_google_sheets_real.py
```

## Project Structure

```
Slack/
├── src/
│   ├── app.py                    # Main Flask application
│   ├── slack_client.py          # Slack API client
│   ├── slack_events.py          # Slack event handlers
│   ├── google_sheets_real.py    # Google Sheets API client
│   ├── test_slack.py            # Slack API tests
│   └── test_google_sheets_real.py # Google Sheets tests
├── .env                         # Environment variables
├── credentials.json             # Google API credentials
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Next Steps

- [ ] Set up ngrok for local development
- [ ] Configure Slack Event Subscriptions
- [ ] Add error handling and logging
- [ ] Implement message filtering
- [ ] Add Slack slash commands
- [ ] Deploy to production