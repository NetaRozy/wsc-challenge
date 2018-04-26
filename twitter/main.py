from twitter_actions import *
import utils


def filter_tweets_by_word(tweets, word):

    filtered_tweets = []

    for tweet in tweets:
        if word in tweet.text.lower():
            filtered_tweets.append(tweet)

    return filtered_tweets




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

    data = utils.read_json('files/data.json')

    tweets = get_tweets_from_query("#wscchallenge")

    print(len(filter_tweets_by_word(tweets, 'slovenia')))

