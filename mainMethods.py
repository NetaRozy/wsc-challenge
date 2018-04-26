import time
import wscHelperMethods


def get_game_highlights(home, visitor):

    home_id = wscHelperMethods.get_team_id(home)
    visitor_id = wscHelperMethods.get_team_id(visitor)

    game_id = wscHelperMethods.get_game(home_id, visitor_id)
    video_id = wscHelperMethods.create_highlights(game_id)

    time.sleep(60)

    return video_id

def get_game_highlights_by_event(home, visitor, event):

    home_id = wscHelperMethods.get_team_id(home)
    visitor_id = wscHelperMethods.get_team_id(visitor)

    game_id = wscHelperMethods.get_game_id(home_id, visitor_id)
    event_id = wscHelperMethods.events[event]

    event_ids = wscHelperMethods.get_event_ids(game_id=game_id, action_id=event_id)

    video_id = wscHelperMethods.create_event_video_id(event_ids, home+visitor+event)

    time.sleep(60)

    return wscHelperMethods.get_video_url(video_id)



