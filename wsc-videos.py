import requests
import json
import time

headers = {
    'Authorization': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1laWQiOjEwMDA1NSwidW5pcXVlX25hbWUiOjEwMDAwMDU3OSwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvc3lzdGVtIjoxMDEsIlRlYW1zUGVybWlzc2lvbnMiOiJbXSIsImlzcyI6InNlbGYiLCJhdWQiOiJodHRwOi8vY2xpcHJvLnR2IiwiZXhwIjoxNTI0OTIxMzc4LCJuYmYiOjE1MjQ2NjIxNzh9.TiM-E651s1udWsLh55bh8Uijynq1LCVTkD6Wfz__TnY",
    'Accept': "application/json",
    'Content-Type': 'application/json'
}

url = "http://hacktonexternalapi.azurewebsites.net/Api/"


def get_game_id():

    prms = {'request.systemType' : 'Eurobasket'}

    #get the first game id
    get_game_ids = requests.request("GET", url+"SearchGames", headers=headers, params=prms)

    j = json.loads(get_game_ids.text)
    game_id = j['objects'][0]['id']
    return game_id

def create_highlights (game_id):

    #create highlights
    prms = {
      "systemType": "Eurobasket",
      "gameId": game_id,
      "videoLength": "00:00:30"
    }

    time.sleep(10)

    vid_rule_id = requests.request("POST", url+"CreateGameHighlights", headers=headers, json=prms)

    return json.loads(vid_rule_id.text)['ruleId']



def get_video_id(rule_id):
#get the video id
    # url_video_id = 'http://hacktonexternalapi.azurewebsites.net/Api/GetVideoId'

    prms = {
      "ruleId": rule_id
    }

    time.sleep(10)


    vid_id = requests.request("GET", url+"GetVideoId", headers=headers, params=prms)
    # print vid_id.text

    return json.loads(vid_id.text)['videoId']




def check_status(video_id):
    # check status
    url_check_status = 'http://hacktonexternalapi.azurewebsites.net/Api/GetVideoCreationStatus'

    prms = {
      "videoId": video_id
    }

    vid_status = requests.request("GET", url+"GetVideoCreationStatus", headers=headers, params=prms)

    return json.loads(vid_status.text)['videoCreationStatus']

def get_video_url(video_id):

    # get the video url
    url_video_url = 'http://hacktonexternalapi.azurewebsites.net/Api/GetVideoUrl'


    prms = {
        "request.videoId": video_id,
        "request.systemType": "Eurobasket"
    }

    time.sleep(20)
    vid_url = requests.request("GET", url+"GetVideoUrl", headers=headers, params=prms)

    return json.loads(vid_url.text)['videoUrl']


time.sleep(15)

# print get_video_url(get_video_id(create_highlights(get_game_id())))



def get_event_id(game_id=0, action_id=0, team_id=0, player_id=0):

    prms = {"request.systemType": "Eurobasket"}

    if game_id != 0:
        prms['request.gameIds'] = game_id
    if action_id != 0:
        prms['request.actionIds'] = action_id
    if team_id != 0:
        prms['request.teamIds'] = team_id
    if player_id != 0:
        prms['request.playerIds'] = player_id
    # prms = {
    #     "request.gameIds": game_id,
    #     "request.actionIds": action_id,
    #     "request.teamIds": team_id,
    #     "request.playerIds": player_id,
    #     "request.systemType": "BCL"
    # }
    print prms
    event_id = requests.request("GET", url+"SearchClipPbP", headers=headers, params=prms)
    # top_events = {}
    # top_events['game:'+event_id.json()[0]['game']['id']+'team:' ]
    # print event_id.json()[0]['game']['id']
    return event_id.json()


# print get_event_id(game_id=51541, action_id=102)


def create_event_video_id(event_ids, event_name):
    prms = {
        "eventClipIds": [
            event_ids[0]['id'], event_ids[1]['id'], event_ids[2]['id'], event_ids[3]['id'], event_ids[4]['id']
        ],
        "title": "D'Angelo's Miss",
        "systemType": "Eurobasket"
    }

    video_id = requests.request("POST", url+"CreateManual", headers=headers, json=prms)

    return json.loads(video_id.text)['videoId']

# print get_video_url(create_event_video_id(get_event_id(game_id=30088, action_id=102), "testing"))



