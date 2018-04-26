import requests
import json
import time

headers = {
    'Authorization': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1laWQiOjEwMDA1NSwidW5pcXVlX25hbWUiOjEwMDAwMDU3OSwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvc3lzdGVtIjoxMDEsIlRlYW1zUGVybWlzc2lvbnMiOiJbXSIsImlzcyI6InNlbGYiLCJhdWQiOiJodHRwOi8vY2xpcHJvLnR2IiwiZXhwIjoxNTI0OTIxMzc4LCJuYmYiOjE1MjQ2NjIxNzh9.TiM-E651s1udWsLh55bh8Uijynq1LCVTkD6Wfz__TnY",
    'Accept': "application/json",
    'Content-Type': 'application/json'
}

url = "http://hacktonexternalapi.azurewebsites.net/Api/"

events = {'2 PTS': '101', '3 PTS': '102', 'Dunks': '103', 'Assists': '107', 'Blocks': '110'}


def get_game_id(home_id=0, visitor_id=0):

    prms = {'request.systemType' : 'Eurobasket'}

    if home_id != 0:
        prms['request.homeTeamId'] = home_id
    if visitor_id != 0:
        prms['request.visitorTeamIds'] = visitor_id

    #get the first game id
    get_game_ids = requests.request("GET", url+"SearchGames", headers=headers, params=prms)

    j = json.loads(get_game_ids.text)
    game_id = j['objects'][0]['id']
    return game_id

def get_team_id(name):
    prms = {'request.systemType': 'Eurobasket', 'request.text': name}

    get_team_ids = requests.request("GET", url + "SearchTeams", headers=headers, params=prms)

    j = json.loads(get_team_ids.text)
    game_id = j['objects'][0]['id']
    return game_id



# def create_highlights (game_id):
#
#     #create highlights
#     prms = {
#       "systemType": "Eurobasket",
#       "gameId": game_id,
#       "videoLength": "00:00:30"
#     }
#
#     time.sleep(10)
#
#     vid_rule_id = requests.request("POST", url+"CreateGameHighlights", headers=headers, json=prms)
#
#     return json.loads(vid_rule_id.text)['ruleId']


def create_highlights(game_id):

    #create highlights
    prms = {
      "systemType": "Eurobasket",
      "gameId": game_id,
      "videoLength": "00:00:30"
    }

    time.sleep(10)
    vid_rule_id = requests.request("POST", url+"CreateGameHighlights", headers=headers, json=prms)
    rule_id = json.loads(vid_rule_id.text)['ruleId']
    prms = {"ruleId": rule_id}

    time.sleep(10)
    vid_id = requests.request("GET", url+"GetVideoId", headers=headers, params=prms)
    return json.loads(vid_id.text)['videoId']

# def get_video_id(rule_id):
# #get the video id
#     # url_video_id = 'http://hacktonexternalapi.azurewebsites.net/Api/GetVideoId'
#
#     prms = {
#       "ruleId": rule_id
#     }
#
#     time.sleep(10)
#
#
#     vid_id = requests.request("GET", url+"GetVideoId", headers=headers, params=prms)
#     # print vid_id.text
#
#     return json.loads(vid_id.text)['videoId']



def check_status(video_id):
    # check status
    prms = {
      "videoId": video_id
    }

    vid_status = requests.request("GET", url+"GetVideoCreationStatus", headers=headers, params=prms)

    return json.loads(vid_status.text)['videoCreationStatus']

def get_video_url(video_id):

    # get the video url
    prms = {
        "request.videoId": video_id,
        "request.systemType": "Eurobasket"
    }

    time.sleep(60)
    vid_url = requests.request("GET", url+"GetVideoUrl", headers=headers, params=prms)

    return json.loads(vid_url.text)['videoUrl']

# print get_video_url(create_highlights(30088))

time.sleep(15)

# print get_video_url(get_video_id(create_highlights(get_game_id())))



def get_event_ids(game_id=0, action_id=0, team_id=0, player_id=0):

    prms = {"request.systemType": "Eurobasket"}

    if game_id != 0:
        prms['request.gameIds'] = game_id
    if action_id != 0:
        prms['request.actionIds'] = action_id
    if team_id != 0:
        prms['request.teamIds'] = team_id
    if player_id != 0:
        prms['request.playerIds'] = player_id

    # print prms
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
        "title": event_name,
        "systemType": "Eurobasket"
    }

    video_id = requests.request("POST", url+"CreateManual", headers=headers, json=prms)

    return json.loads(video_id.text)['videoId']

def get_my_video(text):
    prms = {"request.systemType": "Eurobasket"}

    if text != '':
        prms['request.searchText'] = text

    # print prms
    videos = requests.request("GET", url + "GetVideos", headers=headers, params=prms)
    # top_events = {}
    # top_events['game:'+event_id.json()[0]['game']['id']+'team:' ]
    # print event_id.json()[0]['game']['id']
    j = json.loads(videos.text)
    video = j['videoResponseObjects'][0]
    return video
#
# vid = get_my_video('serbiaspainDunks')
# print (vid['videoUrl'])
# print (vid['thumbnail']['mediumThumbnailUrl'])
# print get_video_url(create_event_video_id(get_event_id(game_id=30088, action_id=102), "testing"))
