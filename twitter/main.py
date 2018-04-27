from twitter_actions import *
import utils
import mainMethods as wsc
import random
import urllib.request
import moviepy.editor as mp

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

    for word in utils.DATA['GAME_HIGHLIGHTS']:
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

    for word in utils.DATA['PLAYER_HIGHLIGHTS']:
        filtered_tweets += filter_tweets_by_word(tweets, word['word'])


    for tweet in filtered_tweets:
        if tweet.id not in id_list:
            filtered_tweets_set.append(tweet)
            id_list += [tweet.id]

    return filtered_tweets_set

def find_team_names(tweets):

    for tweet in tweets:
        TWEETS_TEAMS[tweet.id] = []
        for team in utils.DATA['TEAMS']:
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
        message = random.choice(greetings) + "! Check out the game highlights on WSC Sports!"

        print("Generating video for tweet " + str(tweet.id))
        video = video_preprocess(team1 + " " + team2, tweet)

        print("Posting to tweeter")
        comment_video(video, message, tweet.id, tweet.author.screen_name)

def video_preprocess(get_video, tweet):
    print("Fetching game highlights from WSC")
    video = wsc.get_my_video(get_video)

    print("Downloading file to server")
    filename = str(tweet.id) + ".mp4"
    urllib.request.urlretrieve(video['videoUrl'], "videos/" + filename)

    print("Shrinking file to match twitters' annoying policy")
    shrink_video(filename)

    return "videos/shrinked_" + filename

def post_team_highlights(tweets):
    # print(len(tweets))
    greetings = ["What a victory", "Great win", "Congratulations"]
    for tweet in tweets:
        team = TWEETS_TEAMS[tweet.id][0]
        to_date = tweet.created_at
        message = random.choice(greetings) + "! Check out your teams' highlights on WSC Sports"

        print("Generating video for tweet " + str(tweet.id))
        video = video_preprocess(team + " top plays", tweet)

        print("Posting to tweeter")
        comment_video(video, message, tweet.id, tweet.author.screen_name)


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

def twitter_scan():
    ## GET TWEETS, CREATE DICTIONARY AND FILTER ALREADY PUBLISHED TWEETS##
    tweets = check_blacklist(get_tweets_from_query("#wscchallenge"))
    gen_tweet_dictionary(tweets)

    ## FILTER FOR GAME / TEAM HIGHLIGHTS ##
    filtered_tweets = filter_game_highlights(tweets)

    find_team_names(filtered_tweets)

    two_teams = filter_2_teams_only()
    one_team = filter_1_team_only()

    # print(two_teams)
    # print(one_team)

    ## POST GAME HIGHLIGHTS
    post_game_hightlights(two_teams)

    ## POST TEAM HIGHLIGHTS
    post_team_highlights(one_team)

    ## ADD ALL TWEETS TO BLACKLIST
    add_to_blacklist(tweets)

def text_process(msg):
    teams = []
    for team in utils.DATA['TEAMS']:
        if team['name'].lower() in msg.lower():
            teams += [team['name'].lower()]

    if len(teams) == 2:
        return teams[0] + " " + teams[1]

    if len(team) == 1:
        return teams[0] + " top plays"

    return 0


if __name__ == '__main__':
    twitter_scan()