import requests

steamUrl = 'http://steamcommunity.com/id/beef/'
url = 'https://steamid.xyz/' + steamUrl

def getMoreInfo(steamUrl):
    url = 'https://steamid.xyz/' + steamUrl
    r = requests.get(url)
    toScrape = str(r.text)
    start = toScrape.find('STEAM_0')
    new = toScrape[start:]
    end = new.find("\"")  # should grab the end of the string... needs testing
    return new[:end]
print(getMoreInfo(steamUrl))
print(url)
