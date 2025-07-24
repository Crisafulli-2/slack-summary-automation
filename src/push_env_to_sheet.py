import os
from dotenv import load_dotenv
from google_sheets_real import GoogleSheetsClient

# Load .env from project root
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(env_path)

SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

# Example data to push (can be replaced with actual Slack info)
data = [
    ["SLACK_APP_ID", os.getenv("SLACK_APP_ID")],
    ["SLACK_CLIENT_ID", os.getenv("SLACK_CLIENT_ID")],
    ["SLACK_CLIENT_SECRET", os.getenv("SLACK_CLIENT_SECRET")],
    ["SLACK_SIGNING_SECRET", os.getenv("SLACK_SIGNING_SECRET")],
    ["SLACK_BOT_TOKEN", os.getenv("SLACK_BOT_TOKEN")],
    ["SLACK_APP_LEVEL_TOKEN", os.getenv("SLACK_APP_LEVEL_TOKEN")],
    ["GOOGLE_CREDENTIALS_FILE", os.getenv("GOOGLE_CREDENTIALS_FILE")],
    ["GOOGLE_SHEET_ID", SHEET_ID],
]


def main():
    print("❌ This script is disabled: Never write environment variables or secrets to Google Sheets.")
    print("Aborting.")
    return

if __name__ == "__main__":
    main()
