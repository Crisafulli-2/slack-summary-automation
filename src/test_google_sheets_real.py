from google_sheets_real import GoogleSheetsClient
from dotenv import load_dotenv

load_dotenv()

def test_real_google_sheets():
    try:
        client = GoogleSheetsClient()
        
        # Test writing a summary - try without sheet name first
        test_summary = "5 messages from 3 users\nMost active: @john\nLatest: Hello world!"
        client.write_slack_summary(test_summary, "A1")
        
        # Test appending a message log
        client.append_message_log("john_doe", "Hello from Slack!", "2025-06-06 12:45:00")
        
        print("✅ Real Google Sheets test completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_real_google_sheets()