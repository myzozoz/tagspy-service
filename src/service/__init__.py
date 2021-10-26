import api

# input: list of tags
# output: list of words with values in dict format, e.g.
# {
#   'word': 'exampleword',
#   'value': 22
# }
def analyze_reviews(tags):
  games = api.fetch_games_with_tags(tags)
  reviews = api.fetch_reviews_for_games(games)
  
  # Code to analyze the reviews goes here

  return  [{
   'word': 'exampleword',
   'value': 22
  }, {
   'word': 'seconword',
   'value': 11
  }]