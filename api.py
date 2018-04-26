import requests
import json

#search for game ids
url_gameids = "http://hacktonexternalapi.azurewebsites.net/Api/SearchGames"

headers = {
    'Authorization': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1laWQiOjEwMDA1NSwidW5pcXVlX25hbWUiOjEwMDAwMDU3OSwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvc3lzdGVtIjoxMDEsIlRlYW1zUGVybWlzc2lvbnMiOiJbXSIsImlzcyI6InNlbGYiLCJhdWQiOiJodHRwOi8vY2xpcHJvLnR2IiwiZXhwIjoxNTI0OTIxMzc4LCJuYmYiOjE1MjQ2NjIxNzh9.TiM-E651s1udWsLh55bh8Uijynq1LCVTkD6Wfz__TnY",
    'Accept': "application/json"
}

prms = {
    'request.systemType' : 'BCL'
}

#get the first game id
get_game_ids = requests.request("GET", url_gameids, headers=headers, params=prms)

j = json.loads(get_game_ids.text)
game_id = j['objects'][0]['id']

#create highlights
url_game_highlight = 'http://hacktonexternalapi.azurewebsites.net/Api/CreateGameHighlights'

headers = {
    'Authorization': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1laWQiOjEwMDA1NSwidW5pcXVlX25hbWUiOjEwMDAwMDU3OSwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvc3lzdGVtIjoxMDEsIlRlYW1zUGVybWlzc2lvbnMiOiJbXSIsImlzcyI6InNlbGYiLCJhdWQiOiJodHRwOi8vY2xpcHJvLnR2IiwiZXhwIjoxNTI0OTIxMzc4LCJuYmYiOjE1MjQ2NjIxNzh9.TiM-E651s1udWsLh55bh8Uijynq1LCVTkD6Wfz__TnY",
    'Accept': "application/json",
    'Content-Type': 'application/json'
    }

prms = {
  "systemType": "BCL",
  "gameId": game_id,
  "videoLength": "00:01:00"
}

vid_rule_id = requests.request("POST", url_game_highlight, headers=headers, json=prms)

#get the video id
url_video_id = 'http://hacktonexternalapi.azurewebsites.net/Api/GetVideoId'

headers = {
    'Authorization': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1laWQiOjEwMDA1NSwidW5pcXVlX25hbWUiOjEwMDAwMDU3OSwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvc3lzdGVtIjoxMDEsIlRlYW1zUGVybWlzc2lvbnMiOiJbXSIsImlzcyI6InNlbGYiLCJhdWQiOiJodHRwOi8vY2xpcHJvLnR2IiwiZXhwIjoxNTI0OTIxMzc4LCJuYmYiOjE1MjQ2NjIxNzh9.TiM-E651s1udWsLh55bh8Uijynq1LCVTkD6Wfz__TnY",
    'Accept': "application/json",
    'Content-Type': 'application/json'
    }

prms = {
  "ruleId": json.loads(vid_rule_id.text)['ruleId']
}

vid_id = requests.request("GET", url_video_id, headers=headers, params=prms)

#get the video url
url_video_url = 'http://hacktonexternalapi.azurewebsites.net/Api/GetVideoUrl'

headers = {
    'Authorization': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1laWQiOjEwMDA1NSwidW5pcXVlX25hbWUiOjEwMDAwMDU3OSwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvc3lzdGVtIjoxMDEsIlRlYW1zUGVybWlzc2lvbnMiOiJbXSIsImlzcyI6InNlbGYiLCJhdWQiOiJodHRwOi8vY2xpcHJvLnR2IiwiZXhwIjoxNTI0OTIxMzc4LCJuYmYiOjE1MjQ2NjIxNzh9.TiM-E651s1udWsLh55bh8Uijynq1LCVTkD6Wfz__TnY",
    'Accept': "application/json",
    'Content-Type': 'application/json'
}

prms = {
    "request.videoId": json.loads(vid_id.text)['videoId'],
    "request.systemType": "BCL"
}

vid_url = requests.request("GET", url_video_url, headers=headers, params=prms)

print json.loads(vid_url.text)['videoUrl']
