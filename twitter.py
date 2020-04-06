import tweepy 
from textblob import TextBlob
import re
access_key ='1025563697622786048-TdUHAZE6d3UO3tOJfdm4QgWbKHt2xw'
access_secret='Y1tfYG2QipeV4oNGmOjCAinyhprrGjzJwSxknfvgG8MEU'
consumer_key = 'ySnXmMkdA3OyhdYqfKepYTpIR'
consumer_secret = 'sU1wZGkukA2JzANEFd0EZZx2AGm04fMzGv1E9YmRmqegbuhJaL'

# Function to extract tweets 
def clean_tweet(tweet): 
    ''' 
    Use sumple regex statemnents to clean tweet text by removing links and special characters
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) \
                                |(\w+:\/\/\S+)", " ", tweet).split()) 
def deEmojify(text):
    '''
    Strip all non-ASCII characters to remove emoji characters
    '''
    if text:
        return text.encode('ascii', 'ignore').decode('ascii')
    else:
        return None
def get_tweets(keyword,_size): 
          
        # Authorization to consumer key and consumer secret 
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
  
        # Access to user's access key and access secret 
        auth.set_access_token(access_key, access_secret) 
  
        # Calling api 
        api = tweepy.API(auth) 
        tweet_list = []
        location_list = []
        time_stamp = []
        twitter_user = []

        for tweet in api.search(q=keyword, lang="en", rpp=_size,tweet_mode='extended',count=1000):
            
            temp = tweet.entities['user_mentions']
            if len(temp)<=0 or tweet.user.location==" ":
                continue
            name_  = temp[0]['name']
            time_stamp.append(tweet.created_at)
            twitter_user.append(name_)
            text = tweet.full_text
            clean_text = clean_tweet(text)
            emojified_text = clean_tweet(clean_text)
            tweet_list.append(emojified_text)
            location_list.append(tweet.user.location)


        return [time_stamp,location_list,twitter_user,tweet_list]

#get_tweets("sdv",12)
'''# Driver code 
if __name__ == '__main__': 
  
    # Here goes the twitter handle for the user 
    # whose tweets are to be extracted. 
    get_tweets("samsung")  '''