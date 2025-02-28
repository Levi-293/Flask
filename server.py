from flask import Flask, request
import requests

app = Flask(__name__)

# Go High Level API URL for creating notifications or handling messages
GHL_API_URL = "https://api.gohighlevel.com/v1/notifications"  # Modify with correct API endpoint

# Your Go High Level API Key
GHL_API_KEY = "pit-daa6f987-bc37-4f55-9e2e-034ebe31566d"

@app.route('/webhook', methods=['POST'])
def webhook():
    # Get the incoming data from Twilio (message details)
    data = request.form
    from_number = data.get('From')  # The phone number that sent the message
    message_body = data.get('Body')  # The content of the WhatsApp message
    
    # You may want to process this message and trigger workflows, update contacts, etc.
    send_message_to_ghl(from_number, message_body)

    return "OK", 200

def send_message_to_ghl(from_number, message_body):
    headers = {
        "Authorization": f"Bearer {GHL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Prepare the payload for the notification to Go High Level
    payload = {
        "message": f"New WhatsApp message from {from_number}: {message_body}",
        "type": "whatsapp_message_notification",
        "contact_number": from_number
    }

    # Send the data to Go High Level via the API
    response = requests.post(GHL_API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        print("Successfully sent notification to Go High Level!")
    else:
        print("Failed to send notification.")

if __name__ == '__main__':
    app.run(debug=True)
