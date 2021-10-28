import requests
import json

MAX_REVIEW_PAGES=1

# input: tag
# output: data response from steamspy tag api
def get_games_with_tag(tag):
  r = requests.get("https://steamspy.com/api.php?request=tag&tag=" + str(tag))
  print(r.text)
  return json.loads(r.text)


def get_reviews_for_game(appid):
  reviews = []
  cursor = '*'
  url = f'https://store.steampowered.com/appreviews/{appid}'

  for i in range(MAX_REVIEW_PAGES): 
    r = requests.get(url, params = {'json': 1, 'num_per_page': 100, 'cursor': cursor})
    data = json.loads(r.text)
    if 'reviews' in data:
      reviews += data['reviews']
    if 'cursor' in data:
      cursor = data['cursor']
    else:
      break

  return reviews