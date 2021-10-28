import requests
import json
from bs4 import BeautifulSoup
import os.path

MAX_TAGS = 1000


raw_html = open('resources/steam_game_tags.html')
soup = BeautifulSoup(raw_html, 'html.parser')
divs = soup('div', class_='span4 d-flex')

tags = set()
tag_dict = {}

#continue where we left off
if os.path.isfile('resources/tag_data.json'):
  print('Existing tag data found')
  otf = open('resources/tag_data.json','r')
  tag_dict = json.load(otf)
  print(len(tag_dict))
  

for div in divs:
  t = div.find('a').text
  if t not in tag_dict:
    tags.add(t)

print(len(tags))



for i, tag in enumerate(tags):
  if not i < MAX_TAGS:
    break
  print(f'Processing tag {i+1}/{min(len(tags), MAX_TAGS)} [{tag}]')

  r = requests.get("https://steamspy.com/api.php?request=tag&tag=" + str(tag))
  game_data = json.loads(r.text)
  games = []
  for g in game_data:
    games.append(g)
  
  tag_dict[tag] = games

  with open('resources/tag_data.json', 'w') as outfile:
    json.dump(tag_dict, outfile)
