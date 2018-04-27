import time
import wscHelperMethods


def get_game_highlights(home, visitor):

    home_id = wscHelperMethods.get_team_id(home)
    visitor_id = wscHelperMethods.get_team_id(visitor)

    game_id = wscHelperMethods.get_game_id(home_id, visitor_id)
    video_id = wscHelperMethods.create_game_highlights(game_id)

    time.sleep(60)

    return wscHelperMethods.get_video_url(video_id)

def get_game_highlights_by_event(home, visitor, event):

    home_id = wscHelperMethods.get_team_id(home)
    visitor_id = wscHelperMethods.get_team_id(visitor)

    game_id = wscHelperMethods.get_game_id(home_id, visitor_id)
    event_id = wscHelperMethods.events[event]

    event_ids = wscHelperMethods.get_event_ids(game_id=game_id, action_id=event_id)

    video_id = wscHelperMethods.create_event_video_id(event_ids, home+visitor+event)

    time.sleep(60)

    return wscHelperMethods.get_video_url(video_id)

# to get the video url: vid['videoUrl'], to get the video thumbnail: vid['thumbnail']['mediumThumbnailUrl']
def get_my_video(text):
    vid = wscHelperMethods.get_my_video(text)
    return vid

# def get_vid_url(vid_id):
#     return wscHelperMethods.get_video_url(vid_id)

# print (get_my_video('spain top plays'))
# print(get_game_highlights('spain','russia'))
# print (get_my_video('slovenia serbia'))
# print (get_my_video('spainsloveniaDunks'))
# print(get_my_video('spainsloveniaDunks')['videoUrl'])
# print(get_my_video('Slovenia vs. Serbia'))
