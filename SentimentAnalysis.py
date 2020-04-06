from profanity_filter import ProfanityFilter
from profanity_check import predict, predict_prob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import nltk
import twitter
import pandas as pd

def preprocess_texts(texts):
  preprocessed_text = []
  stop_words = stopwords.words('english')
  for text in texts: 
    punc = text.translate(str.maketrans('','', string.punctuation))
    tokens = word_tokenize(punc)
    words = [w for w in tokens if not w in stop_words]
    untokenized_text = TreebankWordDetokenizer().detokenize(words)
    preprocessed_text.append(untokenized_text)
  return preprocessed_text


def Predict(texts):
  pf = ProfanityFilter()
  sid = SentimentIntensityAnalyzer()
  labels = []
  for text in texts:
    if(pf.is_profane(text)):
      labels.append(0)
    else:
      ss = sid.polarity_scores(text)
      if(ss['compound'] <= -0.05):
        labels.append(0)
      else:
        labels.append(1)
  return labels

def uploaded_file(path):
  df = pd.read_csv(path)
  print(df.head())

def fetch_tweets(keyword,num_of_tweets):
  time_stamp,location_list,twitter_user,tweet_list = twitter.get_tweets(keyword,num_of_tweets)
  print("successfuly obtained tweets")
  prep_text = preprocess_texts(tweet_list)
  labels = Predict(prep_text)
  df = pd.DataFrame(list(zip(time_stamp,location_list,twitter_user,tweet_list, labels)), columns =['time_stamp','location','user name','text', 'val'])
  df.to_csv('file.csv',index=False)
  for i,j in zip(tweet_list,labels):
    print(i)
    print("\n\n")
    print(j)