import api

# input: list of tags
# output: analyzed data
def analyze_reviews(tags):
  games = api.fetch_games_with_tags(tags)
  reviews = api.fetch_reviews_for_games(games)
  
  # Code to analyze the reviews goes here

  return reviews