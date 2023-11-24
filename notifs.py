import requests

BASE_URL = "https://api.pushover.net/1/messages.json"
with open('screts.json' , 'r') as f:
    secrets = json.load(f)
    TOKEN = secrets['pushover_token']
    USER_KEY = secrets['pushover_user_key']

message = ''
URL = f"{BASE_URL}?token={token}&message={message}&user={USE_KEY}"

response = requests.post(URL)
print(response.text)



