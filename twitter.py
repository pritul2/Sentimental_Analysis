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
def cleanTxt(text):
    text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
    text = re.sub('#', '', text) # Removing '#' hash tag
    text = re.sub('RT[\s]+', '', text) # Removing RT
    text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
     
    return text

def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

def getPolarity(text):
    return  TextBlob(text).sentiment.polarity

def get_tweets(keyword,_size): 
        print(_size)
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
        subjectivity = []
        polarity = []

        for tweet in api.search(q=keyword, lang="en", rpp=_size,tweet_mode='extended',count=_size):
            
            temp = tweet.entities['user_mentions']
            if len(temp)<=0 or tweet.user.location==" ":
                continue
            name_  = temp[0]['name']
            time_stamp.append(tweet.created_at)
            twitter_user.append(name_)
            text = tweet.full_text
            clean_text = clean_tweet(text)
            clean_text = cleanTxt(clean_text)
            emojified_text = clean_tweet(clean_text)

            subjectivity.append(getSubjectivity(emojified_text))
            polarity.append(getPolarity(emojified_text))
            subjectivity.append(getSubjectivity(emojified_text))


            tweet_list.append(emojified_text)
            location_list.append(tweet.user.location)

        return [time_stamp,location_list,twitter_user,subjectivity,polarity,tweet_list]

#get_tweets("sdv",12)
'''# Driver code 
if __name__ == '__main__': 
  
    # Here goes the twitter handle for the user 
    # whose tweets are to be extracted. 
    get_tweets("samsung")  '''