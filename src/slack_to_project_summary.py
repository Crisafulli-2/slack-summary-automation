import os
from datetime import datetime
from google_sheets_real import GoogleSheetsClient
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL_NAME = "integration_testing"  # Change as needed
NUM_MESSAGES = 5
TAB_NAME = "project summary"  # The tab to write to

def get_user_display_name(user_id, token):
    url = f"https://slack.com/api/users.info"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"user": user_id}
    resp = requests.get(url, headers=headers, params=params)
    data = resp.json()
    if data.get("ok") and "user" in data:
        profile = data["user"].get("profile", {})
        return profile.get("display_name") or profile.get("real_name") or user_id
    return user_id

def fetch_last_messages(token, channel_name, num_messages):
    # 1. List channels to find the channel ID
    url = "https://slack.com/api/conversations.list"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"exclude_archived": True, "limit": 1000}
    resp = requests.get(url, headers=headers, params=params)
    data = resp.json()
    if not data.get("ok"):
        print("Error listing channels:", data)
        return []
    channels = data["channels"]
    channel_id = None
    for ch in channels:
        if ch["name"] == channel_name:
            channel_id = ch["id"]
            break
    if not channel_id:
        print(f"Channel '{channel_name}' not found.")
        return []
    # 2. Fetch last N messages
    url = "https://slack.com/api/conversations.history"
    params = {"channel": channel_id, "limit": num_messages}
    resp = requests.get(url, headers=headers, params=params)
    data = resp.json()
    if not data.get("ok"):
        print(f"Error fetching messages for {channel_id}:", data)
        return []
    return list(reversed(data["messages"]))

def main():
    messages = fetch_last_messages(SLACK_BOT_TOKEN, CHANNEL_NAME, NUM_MESSAGES)
    automation_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    rows = []
    print("\n--- MESSAGES FOUND IN SLACK ---")
    for msg in messages:
        ts = float(msg.get('ts', 0))
        dt = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        user_id = msg.get('user', 'bot/system')
        text = msg.get('text', '')
        if user_id != 'bot/system':
            display_name = get_user_display_name(user_id, SLACK_BOT_TOKEN)
        else:
            display_name = user_id
        print(f"[{dt}] {display_name}: {text}")
        rows.append([dt, f"{display_name}: {text}", automation_time])
    print("--- END SLACK MESSAGES ---\n")

    # Write to Google Sheet under 'project summary' tab, below header (lines 24-26)
    client = GoogleSheetsClient()
    client.test_connection(SHEET_ID)
    # Read the tab to find the row with the header (search first 40 rows)
    range_name = f"'{TAB_NAME}'!A1:A40"
    sheet = client.service.spreadsheets().values().get(
        spreadsheetId=SHEET_ID,
        range=range_name
    ).execute()
    values = sheet.get('values', [])
    header_row = None
    for idx, row in enumerate(values):
        if row and row[0].strip().lower() == 'meeting cadence':
            header_row = idx + 1  # 1-based
            break
    if header_row is None:
        print(f"❌ 'Meeting Cadence' header not found in '{TAB_NAME}'. Writing to row 2 instead.")
        start_row = 2
        client.write_data(SHEET_ID, f"'{TAB_NAME}'!A1:C1", ["Meeting Cadence", "Message", "Execution Timestamp"])
    else:
        start_row = header_row + 1
    for i, row in enumerate(rows):
        cell_range = f"'{TAB_NAME}'!A{start_row + i}:C{start_row + i}"
        client.write_data(SHEET_ID, cell_range, row)
    print(f"✅ Wrote {len(rows)} messages from #{CHANNEL_NAME} under 'Meeting Cadence' in '{TAB_NAME}'.")

if __name__ == "__main__":
    main()
