import requests
import json
<<<<<<< HEAD
import datetime
from pymongo import MongoClient

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.fall

=======
import matplotlib.pyplot as plt
>>>>>>> 1bc150dc589ded2c43d30325e9887ebdb38a4b0c

content_type_header = {
    'Content-Type': 'application/json',
}

'''
Sends a post request to login to wrnch.

Returns a header object containing the access token.
'''
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

'''
Submits a new job to wrnch.

Returns the job ID of the submitted job.
'''
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


'''
Gets the processed data from a processed job.

Returns the object of processed data.
'''
def get_job(job_id, login_header):
    actual_response = requests.get('https://api.wrnch.ai/v1/jobs/' + job_id, headers=login_header)
    print('Got Job Response: ')
    return actual_response.text


'''
Adds the location, data and if the user has fallen into the database.

Void
'''
def add_to_job_db(location, data, fallen):
    collection = db.montreal_falls
    to_post = {"lng": location[0], "lat": location[1], "fallen": fallen}
    collection.insert_one(to_post)
    return


'''
Checks if a certain job has been processed already, if processed adds to db.

Void
'''
def process_and_add_job(job_id, login_header):
    job_details = get_job(job_id, login_header)
    response_json = json.loads(job_details)
    if 'message' in response_json:
        return False
    else:
        data = job_details
        is_fall = detect_fall(data)
        location = ['45.3','21.55']
        add_to_job_db(location, data, is_fall)
        return True


'''
Detects a fall depending on data given.

Returns a boolean if the video is considered a fall.
'''
def detect_fall(data):
    print ("detecting fall...")
    data = json.loads(data)
    frames_len = len(data["frames"])
    for i in range(frames_len):

        if len(data["frames"][i]["persons"]) == 0:
            print ("no people!")
        else:
            ankle_pos = data["frames"][i]["persons"][0]["pose2d"]["joints"][1]
            hip_pos = data["frames"][i]["persons"][0]["pose2d"]["joints"][5]
            neck_pos = data["frames"][i]["persons"][0]["pose2d"]["joints"][25]
            frame_num = i

            if ankle_pos < hip_pos:
                return True
    return False


'''
Gets input from python for location and filepath.

Adds job to database.
'''
def take_job():
    val = input("Enter location data (x,y):")

w = open("logins.json", 'r')
login_info = json.load(w)
username = login_info["wrnchLogin"]["username"]
password = login_info["wrnchLogin"]["password"]

login_header = login(username, password)
# job_id = submit_job("data/person_walking.mp4", login_header)
job_id = ""
process_and_add_job(job_id,login_header)
