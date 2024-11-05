from flask import Flask, jsonify
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from flask_cors import CORS
import datatree

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1MBEHLbddcLhem5l24vLuntQ48gNnIPbQCYMjlcrbjXw"
SAMPLE_RANGE_NAME = "A5:Z"

def get_sheets_data():
    creds = None    
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range=SAMPLE_RANGE_NAME
        ).execute()
        return result.get("values", [])
    except HttpError as err:
        print(f"An error occurred: {err}")
        return None

@app.route('/data', methods=['GET'])
def get_data():
    data = get_sheets_data()
    if data is None:
        return jsonify({'error': 'Failed to fetch data'}), 500
    print(data)
    data = datatree.convert_data(data)
    return jsonify({'data': data})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    print("Starting server...")
    app.run(host='0.0.0.0', port=5000, debug=True)