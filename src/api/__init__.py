from src.api import data
import math

MAX_GAMES=15
MAX_REVIEW_PAGES=15

# input: list of tags
# output: list of app ids
def fetch_games_with_tags(tags):
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
    if len(matches) >= MAX_GAMES:
      break
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
  reviewpages = max(math.floor(MAX_REVIEW_PAGES / len(games)), 1)

  reviews = []
  i = 1
  for game in games:
    print(f'Fetching {reviewpages} pages of reviews for game {game} ({i}/{len(games)})')
    reviews += data.get_reviews_for_game(game, reviewpages)
    i += 1

  return reviews
  

def fetch_tags():
  return data.get_tags()