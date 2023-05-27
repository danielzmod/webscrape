import requests
from requests.structures import CaseInsensitiveDict
import sys, time
import json

# Settings
ratelimit=2 # seconds of delay between request
filename = 'data.json'
max_fails = 5 # maximum number of fails before quitting
startidx = 1350 # start and end id to request
endidx = 1514

# Get Cookie and token from chrome.
headers=CaseInsensitiveDict()
headers = {
    "Accept": "application/json, text/plain, */*",
    "Cookie": "XXX", # From chrome...
    "Connection": "keep-alive",
    "Referer": "https://website.org/db",
    "token": "XXXX", # From chrome...
    "X-Requested-With": "XMLHttpRequest",
}
def write_to_file(filename, data):
    listObj = []

    # Try appending, if no file exist. 
    try:
        with open(filename) as fp:
            listObj = json.load(fp)
            listObj.append(data)
    except:
        listObj.append(data)

    with open(filename, 'w+') as json_file:
        json.dump(listObj, json_file, 
                            indent=4,  
                            separators=(',',': '))
    

# The API endpoint to communicate with
base_url_post = "https://website.org/api/"
latest = time.time()

# Set start index and lists for storing response
response_list = []
last_write_id = startidx

for id in range(startidx, endidx):
    # add a time delay between requests
    while (time.time()-latest)<ratelimit:
        time.sleep(0.01) 
    
    # i is number to append to base_url_post
    url_post = base_url_post+str(id)
    # Status printout
    print(f"Getting data for id: {id}, time:{time.time()-latest}")
    # A POST request to the API
    latest = time.time()
    post_response = requests.get(url_post, headers=headers)
    
    # Skip incorrect responses
    if post_response.status_code != 200:
        max_fails = max_fails-1
        print(f"Id: {id}, Status code:{post_response.status_code}. \
            Something went wrong.")
        if max_fails<=0:
            sys.exit()
        continue 
    
    # Store response in a list
    response_list.append(post_response.json())

    # Write to file every N:th response
    if id-last_write_id >= 499 or id==endidx-1:
        write_to_file(filename, response_list) 
        last_write_id = id
        response_list = []
