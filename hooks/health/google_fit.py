import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime
import pickle

# Client secret JSON file downloaded from the Google Cloud Console
CLIENT_SECRET_FILE = '/Users/gabriella/Repos/dashboard/hooks/health/client_secrets_file.json'

# The scopes required for the Fitness API
SCOPES = ['https://www.googleapis.com/auth/fitness.activity.read', 'https://www.googleapis.com/auth/fitness.activity.write']
redirect_uri = 'http://localhost:8080/'


def get_access_token():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES, redirect_uri=redirect_uri)
    credentials = flow.run_local_server()
    # Pickle the credentials
    with open('/Users/gabriella/Repos/dashboard/hooks/health/credentials.pkl', 'wb') as f:
        pickle.dump(credentials, f)
    return credentials

def aggregate_steps(credentials):
    now = datetime.datetime.utcnow()
    yesterday = now - datetime.timedelta(days=1)
    start_time = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    end_time = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)

    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

    url = 'https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate'
    headers = {'Authorization': f'Bearer {credentials.token}', 'Content-Type': 'application/json'}
    params = {
        "aggregateBy": [
            {
                "dataTypeName": "com.google.step_count.delta",
                "dataSourceId": "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"
            }
        ],
        "bucketByTime": { "durationMillis": 86400000 },
        "startTimeMillis": int(start_time.timestamp() * 1000),
        "endTimeMillis": int(end_time.timestamp() * 1000)
    }
    response = requests.post(url, headers=headers, json=params)
    return response.json()

if __name__ == "__main__":
    get_access_token()
    def open_credentials():
        with open('/Users/gabriella/Repos/dashboard/hooks/health/credentials.pkl', 'rb') as f:
            credentials = pickle.load(f)
        return credentials

    credentials = open_credentials()
    aggregated_steps = aggregate_steps(credentials)
    print(f"Aggregated Steps for Today: {aggregated_steps}")


