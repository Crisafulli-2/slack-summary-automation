from flask import Flask, request, make_response
from dotenv import load_dotenv
import os
from slack_events import handle_event

load_dotenv()

app = Flask(__name__)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.get_json()
    if data.get("type") == "url_verification":
        return make_response(data.get("challenge"), 200, {"content_type": "application/json"})
    if data.get("type") == "event_callback":
        return handle_event(data)
    return make_response("OK", 200)

if __name__ == "__main__":
    app.run(port=3000)