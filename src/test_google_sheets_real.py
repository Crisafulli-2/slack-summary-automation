from google_sheets_real import GoogleSheetsClient
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def test_real_google_sheets():
    try:
        client = GoogleSheetsClient()
        
        # Test writing a summary - try without sheet name first
        test_summary = "5 messages from 3 users\nMost active: @john\nLatest: Hello world!"
        client.write_slack_summary(test_summary, "A1")
        
        # Generate actual timestamp like slack_events.py does
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Test appending a message log
        client.append_message_log("Justin Test", "Hello from Slack!", timestamp)
        
        print("✅ Real Google Sheets test completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_real_google_sheets()