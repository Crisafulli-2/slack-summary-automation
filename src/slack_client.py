import os
import requests
from datetime import datetime

class SlackClient:
    def __init__(self):
        self.token = os.getenv("SLACK_BOT_TOKEN")
        self.headers = {"Authorization": f"Bearer {self.token}"}
        self.base_url = "https://slack.com/api"
    
    def get_channel_history(self, channel_id, limit=100):
        """Fetch messages from a Slack channel"""
        url = f"{self.base_url}/conversations.history"
        params = {
            "channel": channel_id,
            "limit": limit
        }
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()