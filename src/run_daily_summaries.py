#!/usr/bin/env python3
"""
Daily Slack Channel Summaries - Production Script
Generates comprehensive summaries from Slack channels and writes to Google Sheets
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from slack_summary_reader import SlackSummaryReader
from google_sheets_real import GoogleSheetsClient
from datetime import datetime

def run_daily_summaries():
    """Generate daily summaries for all accessible channels"""
    print("📊 Generating Daily Slack Channel Summaries")
    print("=" * 50)
    
    slack = SlackSummaryReader()
    sheets = GoogleSheetsClient()
    sheet_id = "13raU31sm8wDz1xCQ5WpmHPbmlYgxRok1OLaH1uvJgPo"
    
    # Target channels - add more as bot gets invited
    target_channels = [
        "yahoo-transmit-video-integration",
        "transmit-customer-epg",
        "gotham-ops",
        "transmitops",
        "general",
        "engineering"
    ]
    
    working_summaries = []
    accessible_channels = []
    
    print(f"🔍 Checking {len(target_channels)} target channels...")
    
    for channel in target_channels:
        print(f"\n📋 Processing #{channel}...")
        summary = slack.get_channel_summary(channel, 24)
        
        if "not found" in summary:
            print(f"   ❌ Channel not visible to bot")
        elif "Bot not in channel" in summary:
            print(f"   ⚠️  Bot needs invitation: /invite @google_sheet_test")
        elif "No activity" in summary:
            print(f"   ✅ Accessible but quiet")
            accessible_channels.append(channel)
            working_summaries.append(summary)
        else:
            print(f"   ✅ Active with data!")
            accessible_channels.append(channel)
            working_summaries.append(summary)
    
    # Write results to Google Sheets
    if working_summaries:
        print(f"\n📝 Writing {len(working_summaries)} summaries to Google Sheets...")
        
        if sheets.test_connection(sheet_id):
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Clear and write header
            sheets.clear_sheet(sheet_id)
            sheets.write_data(sheet_id, "A1", f"Daily Slack Channel Summaries - {timestamp}")
            
            # Write each summary
            row = 3
            for i, channel in enumerate(accessible_channels):
                sheets.write_data(sheet_id, f"A{row}", f"=== #{channel} ===")
                sheets.write_data(sheet_id, f"A{row+1}", working_summaries[i])
                row += 4  # Space between summaries
            
            print(f"✅ Successfully written summaries for {len(accessible_channels)} channels!")
            print(f"🔗 View: https://docs.google.com/spreadsheets/d/{sheet_id}")
            
            # Summary stats
            print(f"\n📊 SUMMARY STATS:")
            print(f"   • Accessible channels: {len(accessible_channels)}")
            print(f"   • Channels needing bot invitation: {len(target_channels) - len(accessible_channels)}")
            print(f"   • Integration status: {'✅ Operational' if accessible_channels else '⚠️ Needs setup'}")
            
            return True
        else:
            print("❌ Failed to connect to Google Sheets")
            return False
    else:
        print("\n⚠️  No accessible channels found. Next steps:")
        print("1. Invite bot to channels: /invite @google_sheet_test")
        print("2. Bot needs to be added to private channels manually")
        print("3. Re-run this script after adding bot to channels")
        return False

if __name__ == "__main__":
    success = run_daily_summaries()
    exit(0 if success else 1)
