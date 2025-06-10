#!/usr/bin/env python3
"""
Simple Slack to Google Sheets Integration
Reads channel summaries and writes to Google Sheets
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from slack_summary_reader import SlackSummaryReader
from google_sheets_real import GoogleSheetsClient

def main():
    """Main integration function"""
    load_dotenv()
    
    print("🔄 Slack → Google Sheets Integration")
    print("=" * 40)
    
    # Initialize clients
    slack = SlackSummaryReader()
    sheets = GoogleSheetsClient()
    
    # Test connections
    sheet_id = "13raU31sm8wDz1xCQ5WpmHPbmlYgxRok1OLaH1uvJgPo"
    if not sheets.test_connection(sheet_id):
        print("❌ Google Sheets connection failed")
        return
    
    # Get summaries from target channels
    target_channels = ["gotham-ops", "yahoo-transmit-video-integration", "transmitops", "engineering"]
    
    print(f"\n📋 Processing {len(target_channels)} channels...")
    summaries = []
    
    for channel in target_channels:
        print(f"  • #{channel}")
        summary = slack.get_channel_summary(channel, 24)
        summaries.append(f"#{channel}:\n{summary}\n{'='*50}")
    
    # Write to Google Sheets
    print(f"\n📝 Writing to Google Sheets...")
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Clear sheet and write new data
    sheets.clear_sheet(sheet_id)
    
    # Write header
    header = f"Slack Channel Summaries - {timestamp}"
    sheets.write_data(sheet_id, "A1", header)
    
    # Write summaries
    for i, summary in enumerate(summaries, 2):
        sheets.write_data(sheet_id, f"A{i}", summary)
    
    print(f"✅ Complete! View at: https://docs.google.com/spreadsheets/d/{sheet_id}")

if __name__ == "__main__":
    main()
