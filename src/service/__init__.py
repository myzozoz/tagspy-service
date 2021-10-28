from src import api
from src.service.word_analysis import analyze

# input: list of tags
# output: list of words with values in dict format, e.g.
# {
#   'word': 'exampleword',
#   'value': 22
# }
def analyze_reviews(tags):
  games = api.fetch_games_with_tags(tags)
  reviews = api.fetch_reviews_for_games(games)
  return analyze(reviews)