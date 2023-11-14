import requests

class WakaTime():
    BASE_URL = 'https://wakatime.com/api/v1'

    def __init__(self, api_key):
        self.api_key = api_key
    
    def get_all_time_since_today(self):
        url_extension = f'/users/current/all_time_since_today?api_key={self.api_key}'
        data = (requests.get(self.BASE_URL + url_extension)).json()

        return data

    def all_time_since_today(self):
        data = self.get_all_time_since_today()
        started_at = data['data']['range']['start_date']
        total_seconds = data['data']['total_seconds']
        return {'started_at': started_at, 'total_seconds': total_seconds}
    
    def get_project_commits(self, project):
        url_extension = f'/users/current/projects/{project}/commits?api_key={self.api_key}'
        data = (requests.get(self.BASE_URL + url_extension)).json()

        return data

WakaTime().get_project_commits('Services')


