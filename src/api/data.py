import requests
import json


MAX_REVIEW_PAGES=1
with open('resources/tag_data.json', 'r') as tagfile:
  tag_data = json.load(tagfile)
  tagfile.close()

# input: tag
# output: data response from steamspy tag api
def get_games_with_tag(tag):
  '''
  # In a perfect world we could just fetch everything from the steamspy API,
  # but Cloudflare makes that a pain when deploying to Heroku.
  # Should work locally though
  r = requests.get("https://steamspy.com/api.php?request=tag&tag=" + str(tag))
  return json.loads(r.text)
  '''
  # This method should always work, as long as the tag data has been pre-fetched
  return tag_data[tag]


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