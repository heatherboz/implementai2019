import requests
import json

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
    print('Got Job Response: %s', actual_response.text)
    return actual_response.text


'''
Adds the location, data and if the user has fallen into the database.

Void
'''
def add_to_job_db(location, data, fallen):
    return


'''
Checks if a certain job has been processed already, if processed adds to db.

Void
'''
def process_and_add_job(job_id, login_header):
    job_details = get_job('a3003a2a-104f-4aea-a126-1fb227bf4faf', login_header)
    response_json = json.loads(job_details)
    if 'message' in response_json:
        return False
    else:
        data = job_details
        is_fall = detect_fall(data)
        add_to_job_db(location, data, is_fall)
        return True


'''
Detects a fall depending on data given.

Returns a boolean if the video is considered a fall.
'''
# def detect_fall(data):
#     print ("detecting fall...")
#     data = json.loads(data)
#     frames_len = len(data["frames"])
#     y_vel1 = data["frames"[0]]["head_pose"]["bbox"]["minY"]
#     y_vel2 = data["frames"[frames_len -1]]["head_pose"]["bbox"]["minY"]
#
#     y_vel = (y_vel2 - yvel1)/frames_len
#
#     if y_vel > 5:
#         return True




'''
Gets input from python for location and filepath.

Adds job to database.
'''
def take_job():
    val = input("Enter location data (x,y):")

# w = open("logins.json", 'r')
# login_info = json.load(w)
# username = login_info["wrnchLogin"]["username"]
# password = login_info["wrnchLogin"]["password"]
#
# login_header = login(username, password)
# job_id = submit_job("data/personfalling.jpg", login_header)
# process_and_add_job(job_id,login_header)
