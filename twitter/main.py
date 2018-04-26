from twitter_actions import *
import csv


if __name__ == '__main__':
    video_path = '/Users/yogev/code/hackidc/wsc-challenge/twitter/files/file.mp4'
    #
    # #
    # oauth = oauth_wsc
    # file_path = video_path
    # text = "TEST"
    # tweet_id = 989622896732631041
    # usr_screen_name = '@yogevkr'

    # comment_video(file_path, text, tweet_id, usr_screen_name)

    tweets = get_tweets_from_query("#wscchallenge")

    for tweet in tweets:
        print(tweet.text)

    with open("actors.csv") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        data = [r for r in reader]