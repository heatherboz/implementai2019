import requests
import json
import datetime
import random
from pymongo import MongoClient

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.fall

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
    to_post = {"lng": location[1], "lat": location[0], "fallen": fallen}
    collection.insert_one(to_post)
    return


'''
Checks if a certain job has been processed already, if processed adds to db.

Void
'''
def process_and_add_job(job_id, login_header, job_id_to_video):
    job_details = get_job(job_id, login_header)
    response_json = json.loads(job_details)
    if 'message' in response_json:
        return False
    else:
        data = job_details
        is_fall = detect_fall(data)
        location = get_random_location()
        print("Results for video: %s\n", job_id_to_video[job_id])
        print("---------------------------------------------")
        print("Got random location of: %s\n", location)
        print("Is_Fall: %s\n", is_fall)

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

        if not (len(data["frames"][i]["persons"]) == 0):
            r_ankle_pos = data["frames"][i]["persons"][0]["pose2d"]["joints"][1]
            r_hip_pos = data["frames"][i]["persons"][0]["pose2d"]["joints"][5]
            neck_pos = data["frames"][i]["persons"][0]["pose2d"]["joints"][25]
            head_pos = data["frames"][i]["persons"][0]["pose2d"]["joints"][33]
            l_ankle_pos = data["frames"][i]["persons"][0]["pose2d"]["joints"][11]
            l_hip_pos = data["frames"][i]["persons"][0]["pose2d"]["joints"][7]

            frame_num = i


            if r_ankle_pos < r_hip_pos:
                print ("right ankle below hip!")
                return True

            if l_ankle_pos < l_hip_pos:
                print("left ankle below hip!")
                return True

            if head_pos >= l_hip_pos:
                print("head below l hip")
                return True

            if head_pos >= r_hip_pos:
                print("head below r hip")
                return True
    print ("no one fell!")
    return False


'''
Gets a random location and returns it's longitude and latitude.

Returns a location array of format: [x,y].
'''
def get_random_location():
    locations = [[45.508596, -73.571207], [45.512754, -73.573411], [45.509999, -73.570449], [45.509438, -73.573591], [45.510591, -73.570255], [45.507900, -73.575029],[45.506199, -73.572583], [45.503358, -73.579510], [45.503080, -73.579016], [45.502651, -73.578093], [45.497663, -73.577832]]
    return (random.choice(locations))


'''
Gets input from python for location and filepath.

Adds job to database.
'''
def take_job():
    val = input("Enter location data (x,y):")


'''
Ask for update.

Asks user for update!
'''
def ask_update():
    txt_to_input = raw_input ("Do you want to check if videos are processed?")
    return

w = open("logins.json", 'r')
login_info = json.load(w)
username = login_info["wrnchLogin"]["username"]
password = login_info["wrnchLogin"]["password"]

login_header = login(username, password)

list_of_job_ids = []
videos_seen = []

job_id_to_video = {}

while(True):
    not_yet_submitted_videos = list(set(login_info["videos"]) - set(videos_seen))

    # Submits all outstanding jobs
    for video in not_yet_submitted_videos:
        job_id = submit_job(video, login_header)
        videos_seen.append(video)
        list_of_job_ids.append(job_id)
        job_id_to_video[job_id] = video

    print("Videos to Process: \n")
    for key in list_of_job_ids:
        print(job_id_to_video[key])
    # Asks for update.
    ask_update()

    # Once asked for update, attempts to process and add each job in list of ids
    copy_of_list = list_of_job_ids
    for job in copy_of_list:
        if process_and_add_job(job,login_header,job_id_to_video):
            list_of_job_ids.remove(job)
