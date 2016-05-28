import requests
from nosbot import NewsItem
from datetime import datetime, timedelta
from asyncio import Lock


class NewsDataSource:

    def __init__(self, fetchUrl):
        self.cached_news = []
        self.fetchUrl = fetchUrl
        self._update_news_cache()
        self.last_sort_time = datetime.min
        self.sort_lock = Lock()

    def get_top_news(self, amount):
        if datetime.now() - self.last_sort_time > timedelta(minutes=5):
            yield from self.sort_lock
            self.cached_news.sort(key=lambda news_item: news_item.interesting_counter, reverse=True)
            self.sort_lock.release()

        return self.cached_news[:amount]

    def _update_news_cache(self):
        r = requests.get(self.fetchUrl)

        json = r.json()
        for entry in json['items']:
            self.cached_news.append(NewsItem.NewsItem(entry))

if __name__ == '__main__':
    s = NewsDataSource('http://s.nos.nl/extern/nieuws.json')