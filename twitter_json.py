import tweepy 
from textblob import TextBlob
import re
import json




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
        print(_size)
        input("pritul")
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

        '''for tweet in api.search(q=keyword, lang="en", rpp=_size,tweet_mode='extended',count=_size):
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
                                    location_list.append(tweet.user.location)'''

        f = open('data.txt','w')
        cnt = 0
        for tweet in api.search(q=keyword, lang="en", rpp=_size,tweet_mode='extended',count=_size):
            json.dump(tweet._json,fp=f, indent=4, separators=(',', ': '))
            f.write("\n")
            cnt+=1
        f.close()
        input("done"+str(cnt))
        return [time_stamp,location_list,twitter_user,tweet_list]


get_tweets('modi',10)
with open('data.txt') as f:
    for jsonObj in f:
        print(jsonObj)
