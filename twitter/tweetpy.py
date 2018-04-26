import tweepy
from twython import Twython
from oauths import usr_auth
from oauths import yogev_auth


def bot_tweets():

    # //////// Configurations ////////

    auth = tweepy.OAuthHandler(usr_auth.OAUTH_TOKEN, usr_auth.OAUTH_TOKEN_SECRET)
    auth.set_access_token(auth.access_token, auth.access_token_secret)

    api = tweepy.API(auth)

    # //////// Search ////////

    tweets = api.search(q="#wscchallenge")

    for tweet in tweets:
        print(tweet.text + "\n")


    # //////// Write a tweet /////////

    # api.update_status("Text")

    # //////// Comment ////////

    status_id = tweets[0].id
    status_screen_name = tweets[0].user.screen_name


    text = 'WOW! @{}'.format(status_screen_name)


    # api.update_status(text, in_reply_to_status_id=status_id)
    # file_path = '/Users/yogev/code/hackidc/wsc-challenge/twitter/files/index.png'

    # api.update_with_media(file_path, status=text, in_reply_to_status_id=status_id)






    # public_tweets = api.home_timeline()
    # for tweet in public_tweets:
    #     print tweet.text


def yogev_tweets():

    auth = tweepy.OAuthHandler(yogev_auth.OAUTH_TOKEN, yogev_auth.OAUTH_TOKEN_SECRET)
    auth.set_access_token(yogev_auth.APP_KEY, yogev_auth.APP_SECRET)

    api = tweepy.API(auth)

    public_tweets = api.home_timeline()

    api.update_status("!")


def upload_video_twython(auth):
    twitter = Twython(usr_auth.APP_KEY, usr_auth.APP_SECRET,
                      usr_auth.OAUTH_TOKEN, usr_auth.OAUTH_TOKEN_SECRET)

    video = open('/Users/yogev/code/hackidc/wsc-challenge/twitter/files/film.mp4', 'rb')
    response = twitter.upload_video(media=video, media_type='video/mp4')
    twitter.update_status(status='WSC!', media_ids=[response['media_id']])


def main():
    bot_tweets()


if __name__ == "__main__":
    main()