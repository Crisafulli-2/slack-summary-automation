
# Slack to Google Sheets Integration

**Automated system to extract Slack channel messages and summaries using the Slack API, and save them to Google Sheets.**

## ✅ CURRENT SCRIPTS & FUNCTIONS

- **`simple_slack_api_recap.py`**: Lists all public Slack channels and prints the last 5 messages from the first channel, showing timestamp, user display name, and message text. Uses the Slack Web API.
- **`push_general_to_project_summary.py`**: Fetches recent messages from a Slack channel, resolves user IDs to display names, deduplicates by timestamp, and writes/updates rows in a Google Sheet (project summary tab). Adds runtime and channel link columns.
- **`google_sheets_real.py`**: Handles Google Sheets API integration (read/write/update/clear rows).
- **`check_bot_membership.py`**: Checks if the Slack bot is a member of a given channel.
- **Other scripts**: (`push_env_to_sheet.py`, `quick_recap_extraction.py`) are utilities for specialized extraction or data push tasks.

## 🚀 QUICK START

1. **List channels and print last 5 messages:**
   ```bash
   cd src
   python3 simple_slack_api_recap.py
   ```

2. **Push Slack messages to Google Sheets:**
   ```bash
   cd src
   python3 push_general_to_project_summary.py
   ```

## SETUP

- Add your Slack Bot Token to a `.env` file in the project root: `SLACK_BOT_TOKEN=...`
- Add your Google Sheets credentials as `credentials.json` in the project root.

## DATA FORMAT

- **Slack message output:** Timestamp, user display name, message text (from `simple_slack_api_recap.py`)
- **Google Sheets output:** Timestamp, channel, user, message, runtime, channel link (from `push_general_to_project_summary.py`)


## LOADING CREDENTIALS LOCALLY (Best Practice)

Secrets like `credentials.json` and `.env` should never be committed to git. To use them locally:

1. Place your `credentials.json` (Google service account) and `.env` (with `SLACK_BOT_TOKEN`, etc.) in the project root.
2. These files are already in `.gitignore` and will not be tracked by git.
3. All scripts will load these files automatically at runtime:
   - Python scripts use `from dotenv import load_dotenv` to load `.env`.
   - Google Sheets API libraries will look for `credentials.json` in the project root.
4. To share credentials with teammates, use a secure channel (never email or commit to git).

**Example .env:**
```env
SLACK_BOT_TOKEN=xoxb-...
GOOGLE_SHEET_ID=...
```

**Example usage in Python:**
```python
from dotenv import load_dotenv
import os
load_dotenv()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
```


✅ **Working** – Slack API integration, user name resolution, deduplication, and Google Sheets writing/updating are all functional.

## NEXT STEPS

- Look into "recap" summaries and see if those can be read
- IF above is not true, then create slack workflow to summarize all intended channels, format it nicely, then output the summary made channel to the account tracker

## 📊 EXTRACTED DATA

The system extracts and saves:
- **Date & Time**: When the data was extracted
- **Active Channels**: Number from "X of your Y recap channels" 
- **Total Channels**: Total channels in workspace
- **Activity Rate**: Percentage of active channels
- **Recap Date**: The date mentioned in the recap
- **Delivered with Love**: Status indicator (✅/❌)
- **Notes**: Automation metadata
- Clean, readable format

✅ **Smart Analysis**
- Identifies conversation topics and themes
- Filters substantial messages from noise
- User mention extraction and resolution
- Professional summary formatting in Slack recap style

## Quick Start

### Method 1: Slack API (Traditional)

#### 1. Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

#### 2. Add API Credentials
Edit `.env` file:
```bash
SLACK_BOT_TOKEN=xoxb-your-bot-token
GOOGLE_CREDENTIALS_FILE=credentials.json
```

#### 3. Add Bot to Slack Channels
In any Slack channel, type:
```
/invite @google_sheet_test
```

#### 4. Run Daily Summaries
```bash
python src/run_daily_summaries.py --method api
```

### Method 2: Web Scraping (NEW!)

#### 1. Extract Browser Authentication
```bash
python src/extract_auth.py
```

Follow the interactive prompts to:
1. Open Slack in your browser
2. Use Developer Tools to copy a cURL request
3. Extract authentication cookies automatically

#### 2. Run Web Scraping
```bash
python src/run_daily_summaries.py --method webscrape
# OR use the generated script:
python src/run_web_scraping.py
```

## Benefits of Web Scraping

🚀 **No Bot Setup Required** - Works immediately with your browser session
📋 **Access All Channels** - Including private channels you're already in
⚡ **Full Message Content** - No truncation, captures complete conversations
🔒 **Uses Your Permissions** - Sees exactly what you can see in Slack
```

## Core Files

- `src/slack_summary_reader.py` - Slack API client and summary generation
- `src/google_sheets_real.py` - Google Sheets API client  
- `src/run_daily_summaries.py` - Main production script
- `credentials.json` - Google Service Account credentials
- `.env` - Environment variables and API tokens

## Setup Details

### Slack Bot Setup
1. Create Slack app at https://api.slack.com/apps
2. Add bot scopes: `channels:history`, `channels:read`, `groups:read`, `users:read`
3. Install app to workspace
4. Copy bot token to `.env`

### Google Sheets Setup  
1. Create Google Cloud project
2. Enable Google Sheets API
3. Create service account
4. Download credentials JSON file
5. Share target spreadsheet with service account email

## Target Channels

Currently configured for:
- `yahoo-transmit-video-integration`
- `transmit-customer-epg` 
- `gotham-ops`
- `transmitops`
- `general`
- `engineering`

Add more channels by inviting the bot and updating the channel list in `run_daily_summaries.py`.

## Output Format

The system generates professional summaries including:
- Channel name and timestamp (UTC/ET/PT)
- Message count and activity level
- Conversation overview with topic detection
- List of @mentioned users (real usernames)
- Recent activity metrics

## Google Sheets Output

Target spreadsheet: [Account Tracker Template](https://docs.google.com/spreadsheets/d/13raU31sm8wDz1xCQ5WpmHPbmlYgxRok1OLaH1uvJgPo)

## Automation

Run daily via cron job:
```bash
# Add to crontab for daily 9am execution
0 9 * * * cd /Users/jcris/Projects/Slack && python src/run_daily_summaries.py
```

## Current Status

✅ **Working Features:**
- Slack API integration with bot token authentication
- Google Sheets API integration with service account
- Channel summary generation with conversation analysis
- Multi-timezone support (UTC/ET/PT)
- Real username resolution from @mentions
- Professional summary formatting

✅ **Successfully Tested:**
- `yahoo-transmit-video-integration` channel (bot is member)
- Google Sheets writing to target spreadsheet
- Complete end-to-end integration

## Next Steps

### Immediate Tasks:
1. **Add bot to remaining target channels:**
   - `transmit-customer-epg` - Need to invite bot: `/invite @google_sheet_test`
   - `gotham-ops` - Need to invite bot: `/invite @google_sheet_test`
   - `transmitops` - Need to invite bot: `/invite @google_sheet_test`
   - `general` - Need to invite bot: `/invite @google_sheet_test`
   - `engineering` - Need to invite bot: `/invite @google_sheet_test`

2. **Verify channel access:**
   ```bash
   python src/run_daily_summaries.py
   ```

3. **Schedule automation:**
   - Set up cron job for daily execution
   - Consider using GitHub Actions for cloud automation

### Enhancement Opportunities:
1. **Multi-column Google Sheets formatting** - Structured data across columns A-H
2. **Enhanced conversation analysis** - Topic detection and sentiment analysis
3. **Slack thread support** - Include threaded conversations in summaries
4. **Historical data** - Archive and track channel activity over time
5. **Notification system** - Alert on high activity or important mentions
6. **Channel activity trends** - Weekly/monthly activity comparisons

### Technical Improvements:
1. **Error handling** - Better resilience for API failures
2. **Rate limiting** - Respect Slack API rate limits
3. **Configuration file** - Move hardcoded values to config
4. **Logging** - Add comprehensive logging for debugging
5. **Unit tests** - Add test coverage for core functionality

### Deployment Options:
1. **Local cron job** - Current approach, runs on local machine
2. **Cloud Functions** - AWS Lambda or Google Cloud Functions
3. **GitHub Actions** - Scheduled workflows
4. **Docker container** - Containerized deployment
5. **Heroku Scheduler** - Simple cloud scheduling

## Troubleshooting

### Common Issues:
- **Channel not found**: Bot needs to be invited to private channels
- **Permission denied**: Check bot scopes in Slack app settings
- **Google Sheets access**: Verify service account has sheet access
- **API rate limits**: Add delays between requests if hitting limits

### Debug Commands:
```bash
# Test Slack API connection
python -c "from src.slack_summary_reader import SlackSummaryReader; s=SlackSummaryReader(); print('✅ Slack API working')"

# Test Google Sheets API connection  
python -c "from src.google_sheets_real import GoogleSheetsClient; g=GoogleSheetsClient(); g.test_connection('13raU31sm8wDz1xCQ5WpmHPbmlYgxRok1OLaH1uvJgPo')"

# List all visible channels
python -c "from src.slack_summary_reader import SlackSummaryReader; s=SlackSummaryReader(); [print(f'{c[\"name\"]} - Member: {c.get(\"is_member\", False)}') for c in s.list_channels()]"
```