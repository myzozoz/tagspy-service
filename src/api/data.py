from api import data

import string 
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.sentiment import SentimentIntensityAnalyzer



def fetch_games_with_tags(tags):
  '''
  tag: list of tags
  output: list of app ids
  ######## COMMENT: should we do it with 1 tag only? 
  '''
  if len(tags) < 1:
    return []

  games = {}
  # fetch games for each singe tag
  for tag in tags:
    games[tag] = data.get_games_with_tag(tag)
  
  # find games that match all tags
  compare = tags[0]
  matches = []

  for game in games[compare]:
    all_tags = True
    for tag in tags[1:]:
      if game not in games[tag]:
        all_tags = False
        break

    if all_tags:
      matches.append(game)

  return matches

# input: list of games
# output: list of reviews for those games
def fetch_reviews_for_games(games):
  if len(games) < 1:
    return []
  print(f'Fetching reviews for {len(games)} games...')

  reviews = []
  i = 1
  for game in games:
    print(f'Fetching reviews for game {i}/{len(games)} ({game})')
    reviews += data.get_reviews_for_game(game)
    i += 1

  return reviews


def preprocess_text(reviews):
    '''
    reviews: all the reviews from all the games of interest
    '''

    # load stopwords
    stopwords = open("stop-word-list.csv", "r").read().strip().split(",")
    stopwords = [i.strip() for i in stopwords]
    
    # call lemmatize object
    lmt = WordNetLemmatizer()
    

    for index, review in enumerate(reviews):
        # lemmatize tokens 
        tokens = [lmt.lemmatize(i) for i in review.lower().split()]
        # remove stopwords
        rv = [j for j in tokens if j not in stopwords]
        s = " ".join(rv)
        # remove each reivew from punctuation 
        reviews[index] = s.translate(str.maketrans('', '', string.punctuation))
    
    # return preprocessed reviews
    return reviews
  

def get_top_features(matrix, vector, corpus):
    '''
    Extract the top keywords from each corpora
    matrix: tfidf fitted matrix
    vector: tfidf vector 
    corpus: (list) preprocessed reviews
    '''

    feature_names = vector.get_feature_names()
    top_kw = list()

    for i in range(len(corpus)):
        # get feature index from the matrix 
        feature_index = matrix[i, :].nonzero()[1]
        # get the scores 
        scores = [matrix[i, x] for x in feature_index]
        # zip the feature_index with its corresponding score
        tfidf_scores = zip(feature_index, scores)
        # get top 10 highest scores 
        top_10 = sorted(list(tfidf_scores), key=lambda x: x[1], reverse=True)[:10]
        # get top 10 corresponding words  
        top10_kw = [(feature_names[pos], score) for (pos, score) in top_10]
        # append to final keyword lsit 
        for kw in top10_kw:
            top_kw.append(kw)

    return top_kw

def BOV(top_kws):
    '''
    Bag of Words: Count the frequency of each tokens
    top_kws: top keywords extracted from top features
    '''
    freq = dict()
    
    for (kw, score) in top_kws:
        if kw in freq:
            freq[kw] += 1
        else:
            freq[kw] = 1

    freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    
    return freq[:200]

def sentiment(kws):
    '''
    Calculate the sentiment of the combined keywords
    kws: top keywords got from BOV
    '''
    # call the pre-trained sentiment object 
    sia = SentimentIntensityAnalyzer()
    # calculate the score 
    score = sia.polarity_scores(" ".join([i for (i, s) in kws]))
    
    return score["compound"]