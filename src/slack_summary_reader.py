import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import pytz

load_dotenv()

class SlackSummaryReader:
    def __init__(self):
        self.bot_token = os.getenv("SLACK_BOT_TOKEN")
        self.base_url = "https://slack.com/api"
        self._user_cache = {}  # Cache for username lookups
        
    def _get_username(self, user_id):
        """Get username from user ID, with caching"""
        if user_id in self._user_cache:
            return self._user_cache[user_id]
            
        headers = {"Authorization": f"Bearer {self.bot_token}"}
        response = requests.get(f"{self.base_url}/users.info", 
                              headers=headers, 
                              params={"user": user_id})
        
        if response.json().get("ok"):
            user_info = response.json().get("user", {})
            username = user_info.get("name", user_id[:8])
            self._user_cache[user_id] = username
            return username
        
        return user_id[:8]  # Fallback to truncated ID
    
    def _format_timezone_output(self, timestamp):
        """Format timestamp in UTC/ET/PT"""
        dt = datetime.fromtimestamp(timestamp, tz=pytz.UTC)
        
        utc_time = dt.strftime('%H:%M UTC')
        et_time = dt.astimezone(pytz.timezone('US/Eastern')).strftime('%H:%M ET')
        pt_time = dt.astimezone(pytz.timezone('US/Pacific')).strftime('%H:%M PT')
        
        return f"{utc_time} / {et_time} / {pt_time}"
        
    def list_channels(self):
        """List all channels the bot can see"""
        headers = {"Authorization": f"Bearer {self.bot_token}"}
        response = requests.get(f"{self.base_url}/conversations.list", 
                              headers=headers, 
                              params={"exclude_archived": "true", "types": "public_channel,private_channel"})
        
        if response.json().get("ok"):
            return response.json().get("channels", [])
        return []
    
    def get_channel_summary(self, channel_name, hours_back=24):
        """Get summary for a specific channel"""
        headers = {"Authorization": f"Bearer {self.bot_token}"}
        
        # Get channel ID
        channel_id = self._get_channel_id(channel_name)
        if not channel_id:
            return f"❌ Channel #{channel_name} not found"
            
        # Get recent messages
        messages = self._get_messages(channel_id, hours_back)
        if isinstance(messages, str):  # Error message
            return messages
            
        return self._format_summary(channel_name, messages)
    
    def _get_channel_id(self, channel_name):
        """Get channel ID by name"""
        headers = {"Authorization": f"Bearer {self.bot_token}"}
        
        # Try public channels first
        response = requests.get(f"{self.base_url}/conversations.list", 
                              headers=headers, 
                              params={"exclude_archived": "true", "types": "public_channel"})
        
        if response.json().get("ok"):
            for channel in response.json().get("channels", []):
                if channel.get("name") == channel_name:
                    return channel.get("id")
        
        # Try private channels
        response = requests.get(f"{self.base_url}/conversations.list", 
                              headers=headers, 
                              params={"exclude_archived": "true", "types": "private_channel"})
        
        if response.json().get("ok"):
            for channel in response.json().get("channels", []):
                if channel.get("name") == channel_name:
                    return channel.get("id")
        
        return None
    
    def _get_messages(self, channel_id, hours_back):
        """Get messages from channel"""
        headers = {"Authorization": f"Bearer {self.bot_token}"}
        oldest = (datetime.now() - timedelta(hours=hours_back)).timestamp()
        
        response = requests.get(f"{self.base_url}/conversations.history",
                              headers=headers,
                              params={"channel": channel_id, "oldest": str(oldest), "limit": 50})
        
        data = response.json()
        if not data.get("ok"):
            error = data.get("error", "unknown")
            if error == "not_in_channel":
                return "⚠️ Bot not in channel. Run: /invite @YourBotName"
            return f"❌ Error: {error}"
            
        return data.get("messages", [])
    
    def _format_summary(self, channel_name, messages):
        """Format channel summary with conversation overview and @mentions"""
        if not messages:
            return f"📭 No activity in #{channel_name}"
        
        # Sort messages by timestamp (oldest first for chronological summary)
        sorted_messages = sorted(messages, key=lambda x: float(x.get("ts", 0)))
        
        # Extract @mentions and build conversation summary
        mentioned_users = set()
        conversation_parts = []
        
        for msg in sorted_messages:
            text = msg.get("text", "")
            timestamp = datetime.fromtimestamp(float(msg.get("ts", 0)))
            
            # Skip very short messages or bot messages
            if len(text) < 10 or msg.get("bot_id"):
                continue
            
            # Extract @mentions from the text
            import re
            mentions = re.findall(r'<@([^>]+)>', text)
            for mention in mentions:
                mentioned_users.add(mention)
            
            # Clean up text for conversation summary - simpler approach
            clean_text = text.replace('<@', '@').replace('>', '')
            clean_text = re.sub(r'<[^>]*>', '', clean_text)  # Remove any remaining tags
            clean_text = clean_text.strip()
            
            if clean_text and len(clean_text) > 15:
                conversation_parts.append(clean_text)
        
        # Create overall conversation summary
        if conversation_parts:
            # Combine all conversation parts for a general summary
            full_conversation = " ".join(conversation_parts)
            
            # Create a summary of the main topics
            if "VPAID" in full_conversation or "ad" in full_conversation.lower():
                topic_summary = "Discussion focused on video ad integration and VPAID ad handling."
            elif "transmit" in full_conversation.lower() and "integration" in full_conversation.lower():
                topic_summary = "Team coordination around Transmit integration testing and deployment."
            elif "stream" in full_conversation.lower() or "VOD" in full_conversation:
                topic_summary = "Discussion about video streaming and VOD content delivery."
            else:
                # Generic summary based on length and activity
                topic_summary = f"Active discussion with {len(conversation_parts)} substantial messages exchanged."
        else:
            topic_summary = "Limited conversation activity in this timeframe."
        
        # Format the summary with timezone info
        now = datetime.now(pytz.UTC)
        current_time_zones = self._format_timezone_output(now.timestamp())
        
        summary = f"""🔸 #{channel_name} Channel Summary
📅 {now.strftime('%B %d, %Y')} at {current_time_zones}
💬 {len(messages)} total messages | {len(conversation_parts)} substantial messages

📝 CONVERSATION OVERVIEW:
{topic_summary}

👥 MENTIONED USERS:
"""
        
        if mentioned_users:
            # Convert user IDs to actual usernames
            usernames = []
            for user_id in list(mentioned_users)[:10]:  # Limit to 10 users
                username = self._get_username(user_id)
                usernames.append(f"@{username}")
            summary += f"   {', '.join(usernames)}"
        else:
            summary += "   No specific user mentions found"
        
        latest_timestamp = float(sorted_messages[-1].get("ts", 0))
        latest_time_zones = self._format_timezone_output(latest_timestamp)
        
        summary += f"""

📊 ACTIVITY METRICS:
   • Time Range: Last 24 hours
   • Most Recent: {latest_time_zones} on {datetime.fromtimestamp(latest_timestamp).strftime('%m/%d')}
   • Channel Activity: {'High' if len(messages) > 10 else 'Moderate' if len(messages) > 3 else 'Low'}
"""
        
        return summary