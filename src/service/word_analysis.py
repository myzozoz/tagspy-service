from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.sentiment import SentimentIntensityAnalyzer
import string

def analyze(review_data):
  '''
  review_data: (list of dicts) raw review data
  '''
  reviews = map_reviews(review_data)
  reviews = preprocess_text(reviews)

  vectorizer = TfidfVectorizer()
  vectors = vectorizer.fit_transform(reviews)
  top_features = get_top_features(vectors, vectorizer, reviews)
  kws = BOV(top_features)
  s = sentiment(kws)

  return {
    'top_features': [{'value': f[0], 'count': f[1]} for f in top_features],
    'top_keywords': kws,
    'sentiment': s
  }


def map_reviews(review_data):
  '''
  review_data: (list of dicts) raw review data
  '''
  return [r['review'] for r in review_data if r['language'] == 'english']

def preprocess_text(reviews):
  '''
  reviews: (list) all the reviews from all the games of interest
  '''
  # load stopwords
  
  stopwords = open("resources/stop-word-list.csv", "r").read().strip().split(",")
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

    feature_names = vector.get_feature_names_out()
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