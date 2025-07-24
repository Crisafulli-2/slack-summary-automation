import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime
from dotenv import load_dotenv

# Load .env from parent directory
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

class GoogleSheetsClient:
    def __init__(self):
        # Simple hardcoded path to credentials
        creds_file = "/Users/jcris/Projects/Slack/credentials.json"
        
        print(f"🔍 Looking for credentials at: {creds_file}")
        print(f"📁 File exists: {os.path.exists(creds_file)}")
        
        if not os.path.exists(creds_file):
            print(f"❌ Credentials file not found!")
            raise FileNotFoundError(f"Credentials file not found: {creds_file}")
        
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
            # Accepts a flat list for a row, or a list of lists for multiple rows
            if isinstance(data[0], list):
                body = {'values': data}
            else:
                body = {'values': [data]}
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

def write_integration_testing_messages(sheet_id, slack_token, channel_name='integration_testing', num_messages=5):
    """
    Fetch last N messages from the given Slack channel and write them to the Google Sheet.
    Each row: [Timestamp, User Display Name, Message Text]
    """
    import requests
    from datetime import datetime

    # 1. List channels to find the channel ID
    url = "https://slack.com/api/conversations.list"
    headers = {"Authorization": f"Bearer {slack_token}"}
    params = {"exclude_archived": True, "limit": 1000}
    resp = requests.get(url, headers=headers, params=params)
    data = resp.json()
    if not data.get("ok"):
        print("Error listing channels:", data)
        return
    channels = data["channels"]
    channel_id = None
    for ch in channels:
        if ch["name"] == channel_name:
            channel_id = ch["id"]
            break
    if not channel_id:
        print(f"Channel '{channel_name}' not found.")
        return

    # 2. Fetch last N messages
    url = "https://slack.com/api/conversations.history"
    params = {"channel": channel_id, "limit": num_messages}
    resp = requests.get(url, headers=headers, params=params)
    data = resp.json()
    if not data.get("ok"):
        print(f"Error fetching messages for {channel_id}:", data)
        return
    messages = data["messages"]

    # 3. Helper to resolve user ID to display name
    def get_user_display_name(user_id):
        url = f"https://slack.com/api/users.info"
        params = {"user": user_id}
        resp = requests.get(url, headers=headers, params=params)
        data = resp.json()
        if data.get("ok") and "user" in data:
            profile = data["user"].get("profile", {})
            return profile.get("display_name") or profile.get("real_name") or user_id
        return user_id

    # 4. Prepare rows (oldest first)
    rows = []
    automation_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("\n--- MESSAGES FOUND IN SLACK ---")
    for msg in reversed(messages):
        ts = float(msg.get('ts', 0))
        dt = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        user_id = msg.get('user', 'bot/system')
        text = msg.get('text', '')
        if user_id != 'bot/system':
            display_name = get_user_display_name(user_id)
        else:
            display_name = user_id
        print(f"[{dt}] {display_name}: {text}")
        # Only user display name, never Slack ID
        rows.append([dt, f"{display_name}: {text}", f"Automated by Slack2Sheets at {automation_time}"])
    print("--- END SLACK MESSAGES ---\n")

    # 5. Find the 'Meeting Cadence' header in column A (any row)
    client = GoogleSheetsClient()
    client.test_connection(sheet_id)
    sheet = client.service.spreadsheets().values().get(
        spreadsheetId=sheet_id,
        range="A1:A100"
    ).execute()
    values = sheet.get('values', [])
    header_row = None
    for idx, row in enumerate(values):
        if row and row[0].strip().lower() == 'meeting cadence':
            header_row = idx + 1  # 1-based
            break
    if header_row is None:
        print("❌ 'Meeting Cadence' header not found. Writing to A1 instead.")
        start_row = 2
        client.write_data(sheet_id, "A1:C1", ["Meeting Cadence", "Message", "Automation Info"])
    else:
        start_row = header_row + 1

    # Write each Slack message row below the header, only to columns A-C
    for i, row in enumerate(rows):
        cell_range = f"A{start_row + i}:C{start_row + i}"
        client.write_data(sheet_id, cell_range, row)
    print(f"✅ Wrote {len(rows)} messages from #{channel_name} under 'Meeting Cadence'.")
    
    def write_long_text(self, sheet_id, start_row, column, text):
        """Write long text across multiple rows in a single column"""
        try:
            # Split text into lines and write each line to a separate row
            lines = text.split('\n')
            
            # Prepare data for batch update
            data = []
            for i, line in enumerate(lines):
                if line.strip():  # Only write non-empty lines
                    data.append([line])
            
            if data:
                range_name = f"{column}{start_row}:{column}{start_row + len(data) - 1}"
                body = {'values': data}
                
                result = self.service.spreadsheets().values().update(
                    spreadsheetId=sheet_id,
                    range=range_name,
                    valueInputOption='RAW',
                    body=body
                ).execute()
                
                print(f"✅ Wrote {len(data)} lines to column {column} starting at row {start_row}")
                return start_row + len(data) + 1  # Return next available row
            return start_row
        except Exception as e:
            print(f"❌ Failed to write long text: {e}")
            return start_row
    
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
