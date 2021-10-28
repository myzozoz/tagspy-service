import requests
import json
import cloudscraper
import numpy
from bs4 import BeautifulSoup
import concurrent.futures


def get_working_proxies():
  html = requests.get('https://www.free-proxy-list.net/')

  # Parse HTML response
  content = BeautifulSoup(html.text, 'lxml')

  # Extract proxies table
  table = content.find('table')

  # Extract table rows
  rows = table.findAll('tr')

  # Create proxies result list
  results = []

  # Loop over table rows
  for row in rows:
      # Use only non-empty rows
      if len(row.findAll('td')):
          # Append rows containing proxies to results list
          results.append(row.findAll('td')[0].text +':' + row.findAll('td')[1].text)

  # Create proxies final list
  final =[]
  def test(proxy):
      #test each proxy on whether it access steamspy API
      headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'}
      try:
          params = {
              'request': 'tag',
              'tag': 'Trading'
          }
          requests.get('https://steamspy.com/api.php', headers=headers, proxies={'http' : proxy}, timeout=1, params=params)
          final.append(proxy)
      except:
          pass
      return proxy

  #test multiple proxies concurrently
  with concurrent.futures.ThreadPoolExecutor() as executor:
      executor.map(test, results)

  #to print the number of proxies
  print(len(final))

  #save the working proxies to a file
  numpy.save('proxies.npy', final)

MAX_REVIEW_PAGES=1
try:
  numpy.load('proxies.npy')
except:
  get_working_proxies()
finally:
  proxies = numpy.load('proxies.npy')

scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False})

# input: tag
# output: data response from steamspy tag api
def get_games_with_tag(tag):
  print(f'Using proxy: {proxies[0]}')
  # print("https://steamspy.com/api.php?request=tag&tag=" + str(tag))
  r = scraper.get("https://steamspy.com/api.php?request=tag&tag=" + str(tag), proxies={'https:': proxies[0]})
  # print(r.text)
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