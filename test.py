import requests
from bs4 import BeautifulSoup
steamUrl = 'http://steamcommunity.com/id/beefyo/'
url = 'https://steamid.xyz/' + steamUrl

r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

#print(soup.prettify(encoding=None))
print(soup.findAll(name=None, attrs={}, recursive=True, text=True, limit=None, kwargs=''))