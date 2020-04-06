from profanity_filter import ProfanityFilter
from profanity_check import predict, predict_prob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import nltk
import twitter

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('vader_lexicon')

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


keyword = 'samsung'
num_of_tweets = 10
text = twitter.get_tweets(keyword,num_of_tweets)
print("successfuly obtained tweets")
prep_text = preprocess_texts(text)
labels = Predict(prep_text)

for i,j in zip(text,labels):
  print(i)
  print("\n\n")
  print(j)