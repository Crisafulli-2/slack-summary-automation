import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime

class GoogleSheetsClient:
    def __init__(self):
        # Load credentials from environment variable (JSON string)
        creds_json = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
        if creds_json:
            creds_dict = json.loads(creds_json)
            credentials = Credentials.from_service_account_info(creds_dict)
        else:
            # Fallback to credentials file
            credentials = Credentials.from_service_account_file('path/to/credentials.json')
        
        self.service = build('sheets', 'v4', credentials=credentials)
        self.sheet_id = os.getenv("GOOGLE_SHEET_ID")
    
    def write_to_sheet(self, range_name, values):
        """Write data to Google Sheets"""
        body = {'values': values}
        result = self.service.spreadsheets().values().update(
            spreadsheetId=self.sheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()
        return result
    
    def append_to_sheet(self, range_name, values):
        """Append data to Google Sheets"""
        body = {'values': values}
        result = self.service.spreadsheets().values().append(
            spreadsheetId=self.sheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()
        return result

def log_message_to_sheet(user, text, timestamp):
    # TODO: Implement Google Sheets API logic here
    print(f"Would log to sheet: {user}, {text}, {timestamp}")