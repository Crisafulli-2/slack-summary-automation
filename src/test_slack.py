from slack_client import SlackClient
from dotenv import load_dotenv

load_dotenv()

def test_slack_connection():
    client = SlackClient()
    
    # Test API connection by calling auth.test
    import requests
    url = f"{client.base_url}/auth.test"
    response = requests.get(url, headers=client.headers)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("ok"):
            print("✅ Slack API connection successful!")
            print(f"Bot user: {data.get('user')}")
            print(f"Team: {data.get('team')}")
        else:
            print("❌ Slack API error:", data.get("error"))
    else:
        print("❌ HTTP error:", response.status_code)

if __name__ == "__main__":
    test_slack_connection()