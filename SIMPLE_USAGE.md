# Slack API Recap - Usage Guide

## Overview
Extracts Slack channel messages using the Slack Web API and writes summaries to Google Sheets. No web scraping or browser automation is used—everything is API-based for reliability and security.

## Main Scripts
- `simple_slack_api_recap.py`: Lists all public Slack channels and prints the last 5 messages from the first channel, showing timestamp, user display name, and message text.
- `push_general_to_project_summary.py`: Fetches recent messages from a Slack channel, resolves user IDs to display names, deduplicates by timestamp, and writes/updates rows in a Google Sheet (project summary tab). Adds runtime and channel link columns.
- `google_sheets_real.py`: Handles Google Sheets API integration (read/write/update/clear rows).
- `check_bot_membership.py`: Checks if the Slack bot is a member of a given channel.

## Usage

### List channels and print last 5 messages
```bash
cd /Users/jcris/Projects/Slack/src
python3 simple_slack_api_recap.py
```

### Push Slack messages to Google Sheets
```bash
cd /Users/jcris/Projects/Slack/src
python3 push_general_to_project_summary.py
```

## Output
- **Console**: Timestamp, user display name, message text (from `simple_slack_api_recap.py`)
- **Google Sheet**: Timestamp, channel, user, message, runtime, channel link (from `push_general_to_project_summary.py`)

## Setup
- Add your Slack Bot Token to a `.env` file in the project root: `SLACK_BOT_TOKEN=...`
- Add your Google Sheets credentials as `credentials.json` in the project root.

## Status
✅ **Working** – Slack API integration, user name resolution, deduplication, and Google Sheets writing/updating are all functional.
