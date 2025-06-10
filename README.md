# Slack to Google Sheets Integration

Automated system to generate daily channel summaries from Slack and write them to Google Sheets.

## Features

✅ **Channel Summary Generation**
- Reads messages from Slack channels (last 24 hours)
- Generates intelligent conversation overviews
- Extracts @mentioned users with real usernames
- Multi-timezone support (UTC/ET/PT)
- Activity level assessment

✅ **Google Sheets Integration**
- Writes formatted summaries to Google Sheets
- Automatic timestamp and metadata
- Clean, readable format

✅ **Smart Analysis**
- Identifies conversation topics and themes
- Filters substantial messages from noise
- User mention extraction and resolution
- Professional summary formatting

## Quick Start

### 1. Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

### 2. Add API Credentials
Edit `.env` file:
```bash
SLACK_BOT_TOKEN=xoxb-your-bot-token
GOOGLE_CREDENTIALS_FILE=credentials.json
```

### 3. Add Bot to Slack Channels
In any Slack channel, type:
```
/invite @google_sheet_test
```

### 4. Run Daily Summaries
```bash
python src/run_daily_summaries.py
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