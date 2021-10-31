from src import api
from src.service.word_analysis import analyze


def analyze_reviews(tags):
  '''
    Returns top features, keywords and sentiment as dict
    tags: list of tags
  '''
  games = api.fetch_games_with_tags(tags)
  reviews = api.fetch_reviews_for_games(games)
  results = analyze(reviews)
  results['games'] = games
  return results

def fetch_tags():
  return api.fetch_tags()