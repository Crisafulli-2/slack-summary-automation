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
    # Print all accessible channels (name and ID)
    print("\n--- ACCESSIBLE SLACK CHANNELS ---")
    url = "https://slack.com/api/conversations.list"
    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
    params = {"exclude_archived": True, "limit": 1000}
    resp = requests.get(url, headers=headers, params=params)
    data = resp.json()
    if data.get("ok"):
        for ch in data["channels"]:
            print(f"Channel: {ch['name']} (ID: {ch['id']})")
    else:
        print("Error fetching channels:", data)
    messages = fetch_last_messages(SLACK_BOT_TOKEN, CHANNEL_NAME, NUM_MESSAGES)
    automation_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    rows = []
    print("\n--- MESSAGES FOUND IN SLACK ---")
    # Build a user ID to display name map for all users in the workspace
    def build_user_map(token):
        url = "https://slack.com/api/users.list"
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(url, headers=headers)
        data = resp.json()
        user_map = {}
        if data.get("ok"):
            for user in data["members"]:
                uid = user["id"]
                profile = user.get("profile", {})
                display = profile.get("display_name") or profile.get("real_name") or uid
                user_map[uid] = display
        return user_map

    user_map = build_user_map(SLACK_BOT_TOKEN)

    import re
    mention_pattern = re.compile(r'<@([A-Z0-9]+)>')

    for msg in messages:
        ts = float(msg.get('ts', 0))
        dt = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        user_id = msg.get('user', 'bot/system')
        text = msg.get('text', '')
        # Replace all <@Uxxxx> with display names in the message body
        def replace_mention(match):
            uid = match.group(1)
            return user_map.get(uid, uid)
        text_clean = mention_pattern.sub(replace_mention, text)
        if user_id != 'bot/system':
            display_name = user_map.get(user_id, user_id)
        else:
            display_name = user_id
        # Format: Name appears only at the start, in bold, message body as in Slack
        formatted_message = f"**{display_name}**: {text_clean.strip()}"
        print(f"[{dt}] {display_name}: {text_clean.strip()}")
        rows.append([dt, formatted_message])
    print("--- END SLACK MESSAGES ---\n")

    # Only write if there are messages to write
    if not rows:
        print("No Slack messages found. Nothing written to the sheet.")
        return

    client = GoogleSheetsClient()
    client.test_connection(SHEET_ID)
    # Write headers to line 27 (do not change them)
    header_row = 27
    # Write messages starting at line 28, only to columns A and B
    for i, row in enumerate(rows):
        cell_range = f"'{TAB_NAME}'!A{header_row + 1 + i}:B{header_row + 1 + i}"
        client.write_data(SHEET_ID, cell_range, row)
    # Write automation run time only once in column C, at the first message row
    client.write_data(SHEET_ID, f"'{TAB_NAME}'!C{header_row + 1}", [automation_time])
    print(f"✅ Wrote {len(rows)} messages from #{CHANNEL_NAME} to '{TAB_NAME}' starting at row {header_row + 1}.")

if __name__ == "__main__":
    main()
