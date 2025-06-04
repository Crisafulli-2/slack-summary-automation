from flask import make_response

def handle_event(data):
    print("DEBUG: Received event data:", data)  # Debug print
    event = data.get("event", {})
    if event.get("type") == "message" and "subtype" not in event:
        user = event.get("user")
        text = event.get("text")
        ts = event.get("ts")
        print(f"Message from {user} at {ts}: {text}")
    return make_response("OK", 200)