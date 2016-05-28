import requests
import nosbot.NewsItem

class NewsDataSource:

    def __init__(self, fetchUrl):
        self.cachedNews = []
        self.fetchUrl = fetchUrl
        self.update_news_cache()

    def update_news_cache(self):
        r = requests.get(self.fetchUrl)

        json = r.json()
        for entry in json['items']:
            self.cachedNews.append(nosbot.NewsItem.NewsItem(entry))

if __name__ == '__main__':
    s = NewsDataSource('http://s.nos.nl/extern/nieuws.json')