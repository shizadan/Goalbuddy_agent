from flask import Flask, request
from twilio.rest import Client
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

app = Flask(__name__)

# Twilio credentials
TWILIO_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP = os.environ.get("TWILIO_WHATSAPP")
MY_WHATSAPP = os.environ.get("MY_WHATSAPP")

client = Client(TWILIO_SID, TWILIO_AUTH)

# Google Sheets setup (load from env var)
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(os.environ.get("GOOGLE_CREDS"))
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
gc = gspread.authorize(creds)
sheet = gc.open("Goal_tracking_auto_summary").sheet1

@app.route('/')
def home():
    return "GoalBuddy Bot is running!"

@app.route('/send', methods=['POST'])
def send_message():
    message = client.messages.create(
        from_=f"whatsapp:{TWILIO_WHATSAPP}",
        to=f"whatsapp:{MY_WHATSAPP}",
        body="🚀 Daily reminder from GoalBuddy!"
    )
    return str(message.sid)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
