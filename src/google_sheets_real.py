import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime

class GoogleSheetsClient:
    def __init__(self):
        # Load credentials from file
        creds_file = os.getenv("GOOGLE_CREDENTIALS_FILE")
        credentials = Credentials.from_service_account_file(
            creds_file,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        
        self.service = build('sheets', 'v4', credentials=credentials)
        self.sheet_id = os.getenv("GOOGLE_SHEET_ID")
        print(f"✅ Connected to Google Sheets: {self.sheet_id}")
    
    def write_slack_summary(self, summary_data, cell_range="'Slack Summary'!A1"):
        """Write Slack channel summary to Google Sheets"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        formatted_data = f"Slack Channel Summary - {timestamp}\n{summary_data}"
        
        body = {'values': [[formatted_data]]}
        result = self.service.spreadsheets().values().update(
            spreadsheetId=self.sheet_id,
            range=cell_range,  # Use 'Slack Summary'!A1
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print(f"✅ Wrote to {cell_range}: {formatted_data}")
        return result
    
    def append_message_log(self, user, message, timestamp):
        """Append a message log to the sheet"""
        row_data = [[timestamp, user, message]]
        
        body = {'values': row_data}
        result = self.service.spreadsheets().values().append(
            spreadsheetId=self.sheet_id,
            range="'Slack Summary'!A:C",  # Use 'Slack Summary'!A:C
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print(f"✅ Appended row: {row_data[0]}")
        return result