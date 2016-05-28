import requests
import nosbot.NewsItem
from datetime import datetime, timedelta
from asyncio import Lock


class NewsDataSource:

    def __init__(self, fetch_url):
        self.cached_news = []
        self.fetchUrl = fetch_url
        self._update_news_cache()
        self.last_sort_time = datetime.min
        self.sort_lock = Lock()

    def get_top_news(self, amount, topic_list=[]):
        if datetime.now() - self.last_sort_time > timedelta(minutes=5):
            yield from self.sort_lock
            self.cached_news.sort(key=lambda news_item: news_item.interesting_counter, reverse=True)
            self.sort_lock.release()

        if len(topic_list) == 0:
            return self.cached_news[:amount]
        else:
            return (item for item in self.cached_news if NewsDataSource._news_item_contains_any_topic(item, topic_list))[:amount]

    @staticmethod
    def _news_item_contains_any_topic(newsItem, topics_list):
        for topic in newsItem.categories:
            if topic.name in topics_list:
                return True

        return False

    def _update_news_cache(self):
        r = requests.get(self.fetchUrl)

        json = r.json()
        for entry in json['items']:
            self.cached_news.append(nosbot.NewsItem.NewsItem(entry))

if __name__ == '__main__':
    s = NewsDataSource('http://s.nos.nl/extern/nieuws.json')
