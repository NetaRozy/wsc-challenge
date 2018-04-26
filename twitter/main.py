from twitter_actions import comment_video
from oauths import oauth_wsc

if __name__ == '__main__':
    video_path = '/Users/yogev/code/hackidc/wsc-challenge/twitter/files/file.mp4'

    #
    oauth = oauth_wsc
    file_path = video_path
    text = "TEST"
    tweet_id = 989622896732631041
    usr_screen_name = '@yogevkr'

    comment_video(oauth, file_path, text, tweet_id, usr_screen_name)