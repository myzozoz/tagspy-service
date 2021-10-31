import requests
import json


MAX_REVIEW_PAGES=1

with open('resources/tag_data.json', 'r') as tagfile:
  tag_data = json.load(tagfile)
  tagfile.close()

# In a perfect world we could just fetch everything from the steamspy API,
  # but Cloudflare makes that a pain when deploying to Heroku.
  # Should work locally though
  # This method should always work, as long as the tag data has been pre-fetched
  # Fetch data before hand with scripts/tag_fetch.py
def get_games_with_tag(tag):
  '''
    Returns list of games
    tag: Tag as string
  '''
  
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

def get_tags():
  '''
    Returns list of all possible tags
  '''
  
  return list(tag_data.keys())