import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Helper: Get user display name from Slack user ID
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

# Load .env file from project root
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
print(f"Loading .env from: {env_path}")
load_dotenv(env_path)

# Load Slack Bot Token from environment or .env
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
if not SLACK_BOT_TOKEN:
    raise RuntimeError("SLACK_BOT_TOKEN not set in environment. Please add it to your .env file or export it.")

# Example: List all public channels
def list_channels():
    url = "https://slack.com/api/conversations.list"
    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
    params = {"exclude_archived": True, "limit": 1000}
    resp = requests.get(url, headers=headers, params=params)
    data = resp.json()
    if not data.get("ok"):
        print("Error listing channels:", data)
        return []
    return data["channels"]

# Example: Fetch recent messages from a channel
def fetch_channel_messages(channel_id, limit=100):
    url = "https://slack.com/api/conversations.history"
    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
    params = {"channel": channel_id, "limit": limit}
    resp = requests.get(url, headers=headers, params=params)
    data = resp.json()
    if not data.get("ok"):
        print(f"Error fetching messages for {channel_id}:", data)
        return []
    return data["messages"]

if __name__ == "__main__":
    print("\n--- SLACK CHANNELS ---")
    channels = list_channels()
    for ch in channels:
        print(f"{ch['name']} ({ch['id']})")

    if channels:
        channel_id = channels[0]['id']
        channel_name = channels[0]['name']
        print(f"\n--- LAST 5 MESSAGES FROM: {channel_name} ---")
        messages = fetch_channel_messages(channel_id, limit=5)
        # Print in chronological order (oldest first)
        for msg in reversed(messages):
            ts = float(msg.get('ts', 0))
            dt = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            user_id = msg.get('user', 'bot/system')
            text = msg.get('text', '')
            if user_id != 'bot/system':
                display_name = get_user_display_name(user_id, SLACK_BOT_TOKEN)
            else:
                display_name = user_id
            print(f"[{dt}] {display_name}: {text}")
    else:
        print("No channels found.")
