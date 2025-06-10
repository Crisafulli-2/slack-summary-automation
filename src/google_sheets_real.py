import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class GoogleSheetsClient:
    def __init__(self):
        creds_file = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
        credentials = Credentials.from_service_account_file(
            creds_file,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        
        self.service = build('sheets', 'v4', credentials=credentials)
    
    def test_connection(self, sheet_id):
        """Test connection to Google Sheets"""
        try:
            sheet_metadata = self.service.spreadsheets().get(spreadsheetId=sheet_id).execute()
            title = sheet_metadata.get('properties', {}).get('title', 'Unknown')
            print(f"✅ Successfully connected to sheet: {title}")
            return True
        except Exception as e:
            print(f"❌ Google Sheets connection failed: {e}")
            return False
    
    def write_data(self, sheet_id, cell_range, data):
        """Write data to a specific cell range"""
        try:
            body = {'values': [[data]]}
            result = self.service.spreadsheets().values().update(
                spreadsheetId=sheet_id,
                range=cell_range,
                valueInputOption='RAW',
                body=body
            ).execute()
            
            print(f"✅ Wrote data to {cell_range}")
            return True
        except Exception as e:
            print(f"❌ Failed to write data: {e}")
            return False
    
    def clear_sheet(self, sheet_id, range_name="A:Z"):
        """Clear data from a sheet range"""
        try:
            result = self.service.spreadsheets().values().clear(
                spreadsheetId=sheet_id,
                range=range_name
            ).execute()
            print(f"✅ Cleared range {range_name}")
            return True
        except Exception as e:
            print(f"❌ Failed to clear sheet: {e}")
            return False
