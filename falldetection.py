import requests
import json

content_type_header = {
    'Content-Type': 'application/json',
}

def login(username, password):
    data = '{"username": "' + username + '","password": "' + password + '"}'
    response = requests.post('https://api.wrnch.ai/v1/login', headers=content_type_header, data=data)
    access_token_json = json.loads(response.text)
    access_token_string = access_token_json['access_token']
    print('Access Token Retrieved:%s\n'%access_token_string)
    headers2 = {
        'Authorization': 'Bearer ' + access_token_string,
    }
    return headers2

def submit_job(video_path, login_header):
    files = {
        'work_type': (None, 'json'),
        'heads': (None, 'true'),
        'media': (video_path, open(video_path, 'rb')),
    }
    response = requests.post('https://api.wrnch.ai/v1/jobs', headers=login_header, files=files)
    job_id_json = json.loads(response.text)
    job_id_string = job_id_json['job_id']

    print('Submitted Job To Wrnch with Job ID:%s\n'%job_id_string)
    return job_id_string

def get_job(job_id, login_header):
    actual_response = requests.get('https://api.wrnch.ai/v1/jobs/' + job_id, headers=login_header)
    print('Got Job Response: '%actual_response.text)
    return actual_response.text

def add_to_job_db(location):




def detect_fall(data, location):
    
