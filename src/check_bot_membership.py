import os
from dotenv import load_dotenv
import requests

# Load .env from project root
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(env_path)

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL_ID = "C07QR3DV82K"  # integration_testing

def check_bot_membership(channel_id):
    url = "https://slack.com/api/conversations.info"
    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}"}
    params = {"channel": channel_id}
    resp = requests.get(url, headers=headers, params=params)
    data = resp.json()
    if not data.get("ok"):
        print(f"Error fetching channel info: {data}")
        return False
    channel = data.get("channel", {})
    is_member = channel.get("is_member", False)
    print(f"Bot is{' ' if is_member else ' NOT '}a member of channel {channel_id} ({channel.get('name', 'unknown')})")
    return is_member

if __name__ == "__main__":
    check_bot_membership(CHANNEL_ID)
