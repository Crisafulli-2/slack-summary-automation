import os
from datetime import datetime
from dotenv import load_dotenv
import requests
from google_sheets_real import GoogleSheetsClient

# Load .env from project root
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(env_path)

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")


def get_last_n_messages(channel_id, n=3):
    url = "https://slack.com/api/conversations.history"
    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
    params = {"channel": channel_id, "limit": n}
    resp = requests.get(url, headers=headers, params=params)
    data = resp.json()
    if not data.get("ok") or not data.get("messages"):
        print(f"No messages found or error fetching messages for channel {channel_id}.")
        return []
    return data["messages"]

def get_user_map():
    """Fetch user ID to display name mapping from Slack API."""
    url = "https://slack.com/api/users.list"
    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
    resp = requests.get(url, headers=headers)
    data = resp.json()
    user_map = {}
    if data.get("ok"):
        for user in data.get("members", []):
            user_id = user.get("id")
            # Prefer display_name, fallback to real_name, then name
            profile = user.get("profile", {})
            display_name = profile.get("display_name") or profile.get("real_name") or user.get("name")
            user_map[user_id] = display_name
    return user_map

def push_channel_summary_to_sheet(channel_id, channel_name="(unknown)"):
    messages = get_last_n_messages(channel_id, n=5)
    print(f"Fetched {len(messages)} messages from channel {channel_id} ({channel_name})")
    if not messages:
        print("No messages to push.")
        return
    import re
    from datetime import datetime as dtmod
    user_map = get_user_map()
    rows = []
    mention_pattern = re.compile(r"<@([A-Z0-9]+)>")
    runtime_ts = dtmod.now().strftime("%Y-%m-%d %H:%M:%S")
    channel_link = f"https://app.slack.com/client/T2AAHSB5F/{channel_id}"
    for msg in reversed(messages):  # Oldest first
        ts = float(msg.get("ts", 0))
        dt = datetime.fromtimestamp(ts)
        user_id = msg.get("user", "bot/system")
        text = msg.get("text", "")
        # Replace user mentions in text with display names
        def replace_mention(match):
            uid = match.group(1)
            return user_map.get(uid, f"@{uid}")
        text_clean = mention_pattern.sub(replace_mention, text)
        # Resolve user name
        user_name = user_map.get(user_id, user_id)
        # Pretty print columns
        col1 = dt.strftime("%Y-%m-%d %H:%M:%S")
        col2 = f"{user_name}: {text_clean}"
        col3 = runtime_ts
        col4 = channel_link
        rows.append([col1, col2, col3, col4])
    print("Rows to write/update:")
    for r in rows:
        print(r)

    client = GoogleSheetsClient()
    client.test_connection(SHEET_ID)
    tab_name = 'project summary'
    range_name = f"{tab_name}!A:D"
    # Fetch existing sheet data
    try:
        existing = client.service.spreadsheets().values().get(
            spreadsheetId=SHEET_ID,
            range=range_name
        ).execute().get('values', [])
    except Exception as e:
        print(f"Warning: Could not fetch existing sheet data: {e}")
        existing = []

    # Build a map of date/time to row index
    existing_map = {row[0]: idx for idx, row in enumerate(existing) if row}
    updated = 0
    # Overwrite rows with matching date/time, else append
    for row in rows:
        date_time = row[0]
        if date_time in existing_map:
            # Overwrite this row
            row_idx = existing_map[date_time] + 1  # 1-based for Sheets API
            update_range = f"{tab_name}!A{row_idx}:D{row_idx}"
            try:
                print(f"Updating row {row_idx} with: {row}")
                resp = client.service.spreadsheets().values().update(
                    spreadsheetId=SHEET_ID,
                    range=update_range,
                    valueInputOption='RAW',
                    body={'values': [row]}
                ).execute()
                print(f"Update response: {resp}")
                updated += 1
            except Exception as e:
                print(f"❌ Failed to update row {row_idx}: {e}")
        else:
            # Append as new row
            try:
                print(f"Appending new row: {row}")
                resp = client.service.spreadsheets().values().append(
                    spreadsheetId=SHEET_ID,
                    range=range_name,
                    valueInputOption='RAW',
                    insertDataOption='INSERT_ROWS',
                    body={'values': [row]}
                ).execute()
                print(f"Append response: {resp}")
                updated += 1
            except Exception as e:
                print(f"❌ Failed to append new row: {e}")
    print(f"✅ Wrote/updated {updated} messages from '{channel_name}' to '{tab_name}' tab.")
