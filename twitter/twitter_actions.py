from async_upload import VideoTweet

def comment_video(oauth, file_path, text, tweet_id, usr_screen_name):
    videoTweet = VideoTweet(file_path, oauth)
    videoTweet.upload_init()
    videoTweet.upload_append()
    videoTweet.upload_finalize()
    videoTweet.tweet_comment(text, usr_screen_name, tweet_id)


##  Check it!!!
def tweet_video(oauth, file_path, text):
    videoTweet = VideoTweet(file_path, oauth)
    videoTweet.upload_init()
    videoTweet.upload_append()
    videoTweet.upload_finalize()
    videoTweet.tweet(text)


def get_tweets_from_query
