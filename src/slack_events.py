from flask import make_response
from google_sheets_real import GoogleSheetsClient
from datetime import datetime

# Initialize the real Google Sheets client
sheets_client = GoogleSheetsClient()

def handle_event(data):
    print("DEBUG: Received event data:", data)  
    event = data.get("event", {})
    if event.get("type") == "message" and "subtype" not in event:
        user = event.get("user")
        text = event.get("text")
        ts = event.get("ts")
        timestamp = datetime.fromtimestamp(float(ts)).strftime('%Y-%m-%d %H:%M:%S')
        print(f"Message from {user} at {timestamp}: {text}")
        
        # Log to Google Sheets using the real client
        sheets_client.append_message_log(user, text, timestamp)
        
    return make_response("OK", 200)