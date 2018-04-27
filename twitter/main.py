from twitter_actions import *
import utils
import mainMethods as wsc
import random
import urllib.request
import moviepy.editor as mp

DATA = utils.read_json('files/db.json')
TWEETS_DICT = {}
TWEETS_TEAMS = {}

def gen_tweet_dictionary(tweets):
    for tweet in tweets:
        TWEETS_DICT[tweet.id] = tweet

def filter_tweets_by_word(tweets, word):

    filtered_tweets = []

    for tweet in tweets:
        if word in tweet.text.lower():
            filtered_tweets.append(tweet)

    return filtered_tweets


def filter_game_highlights(tweets):

    filtered_tweets = []
    id_list = []
    filtered_tweets_set = []

    for word in DATA['GAME_HIGHLIGHTS']:
        filtered_tweets += filter_tweets_by_word(tweets, word['word'])



    for tweet in filtered_tweets:
        if tweet.id not in id_list:
            filtered_tweets_set.append(tweet)
            id_list += [tweet.id]


    return filtered_tweets_set

def filter_player_highlights(tweets):

    filtered_tweets = []
    id_list = []
    filtered_tweets_set = []

    for word in DATA['PLAYER_HIGHLIGHTS']:
        filtered_tweets += filter_tweets_by_word(tweets, word['word'])


    for tweet in filtered_tweets:
        if tweet.id not in id_list:
            filtered_tweets_set.append(tweet)
            id_list += [tweet.id]


    return filtered_tweets_set

def find_team_names(tweets):

    for tweet in tweets:
        TWEETS_TEAMS[tweet.id] = []
        for team in DATA['TEAMS']:
            if team['name'].lower() in tweet.text.lower():
                TWEETS_TEAMS[tweet.id] += [team['name'].lower()]

def filter_2_teams_only():
    two_teams_tweets = []

    for tweet_id,countries in TWEETS_TEAMS.items():
        if len(countries) == 2:
            two_teams_tweets += [TWEETS_DICT[tweet_id]]

    return two_teams_tweets

def filter_1_team_only():
    one_teams_tweets = []

    for tweet_id,countries in TWEETS_TEAMS.items():
        if len(countries) == 1:
            one_teams_tweets += [TWEETS_DICT[tweet_id]]

    return one_teams_tweets

def post_game_hightlights(tweets):
    # print(len(tweets))
    for tweet in tweets:
        greetings = ["What a victory", "Great win", "Amazing game"]
        team1 = TWEETS_TEAMS[tweet.id][0]
        team2 = TWEETS_TEAMS[tweet.id][1]
        message = "Check out the game highlights on WSC Sports!"
        # print(message)

        print("Generating video for tweet " + str(tweet.id))
        print("Fetching game highlights from WSC")
        video = wsc.get_my_video(team1 + " " + team2)

        print("Downloading file to server")
        filename = str(tweet.id) + ".mp4"
        urllib.request.urlretrieve(video['videoUrl'], "videos/" + filename)

        print("Shrinking file to match twitters' annoying policy")
        shrink_video(filename)

        print("Posting to tweeter")
        comment_video("videos/shrinked_" + filename, message, tweet.id, tweet.author.screen_name)

def post_team_highlights(tweets):
    # print(len(tweets))
    greetings = ["What a victory", "Great win", "Congratulations"]
    for tweet in tweets:
        team = TWEETS_TEAMS[tweet.id][0]
        to_date = tweet.created_at

        print("Generating video for tweet " + str(tweet.id))
        message = "Check out your teams' highlights on WSC Sports"
        # print(message)

        print("Fetching team highlights from WSC")
        video = wsc.get_my_video(team + " top plays")

        print("Downloading file to server")
        filename = str(tweet.id) + ".mp4"
        urllib.request.urlretrieve(video['videoUrl'], "videos/" + filename)

        print("Shrinking file to match twitters' annoying policy")
        shrink_video(filename)

        print("Posting to tweeter")
        comment_video("videos/shrinked_" + filename, message, tweet.id, tweet.author.screen_name)

        # print("files/video.mp3", message, tweet.id, tweet.author.screen_name)

def shrink_video(path):
    clip = mp.VideoFileClip("videos/" + path)
    clip_resized = clip.resize(height=360)
    clip_resized.write_videofile("videos/shrinked_" + path)

def check_blacklist(tweets):
    blacklist = utils.filtered_tweets_id()
    filtered_tweets = []
    for tweet in tweets:
        if str(tweet.id) not in blacklist:
            filtered_tweets += [tweet]

    # print(filtered_tweets)
    return filtered_tweets

def add_to_blacklist(tweets):
    filtered_id_list = []
    for tweet in tweets:
        filtered_id_list += [tweet.id]
    # print(filtered_id_list)
    utils.add_to_blacklist(filtered_id_list)



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

    ## GET TWEETS AND CREATE DICTIONARY ##
    tweets = check_blacklist(get_tweets_from_query("#wscchallenge"))

    #CHECK IF TWEETS ALREADY PROCESSED

    gen_tweet_dictionary(tweets)

    ## FILTER FOR GAME / TEAM HIGHLIGHTS ##
    filtered_tweets = filter_game_highlights(tweets)

    find_team_names(filtered_tweets)

    two_teams = filter_2_teams_only()
    one_team = filter_1_team_only()

    # print(two_teams)
    # print(one_team)
    post_game_hightlights(two_teams)
    post_team_highlights(one_team)

    add_to_blacklist(tweets)

