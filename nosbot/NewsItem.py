import datetime
from asyncio import Lock


class NewsItem:

    def __init__(self, json):
        self.id = json['id']
        self.type = json['type']
        self.title = json['title']
        self.description = json['description']
        self.publish_time = datetime.datetime.strptime(json['published_at'], '%Y-%m-%dT%H:%M:%S+%f')
        self.last_modification_time = datetime.datetime.strptime(json['modified_at'], '%Y-%m-%dT%H:%M:%S+%f')

        self.interesting_counter_lock = Lock()
        self.interesting_counter = 0

        if 'image' in json:
            self.main_image_url = json['image']['formats'][0]['url']['jpg']

        self.content = []
        self.categories = []

        for i in json['categories']:
            self.categories.append(NewsCategory(i))

        self._parse_content_json_children(json['content']['children'])

    def mark_interesting(self):
        yield from self.interesting_counter_lock
        self.interesting_counter += 1
        self.interesting_counter_lock.release()

    def _parse_content_json_children(self, json):

        for child in json:
            childType = child['type']
            if childType == 'text' or childType == 'title':
                self.content.append(NewsItemContent(child))
            elif childType == 'container':
                self._parse_content_json_children(child['children'])
            elif childType == 'external_content':
                self._read_external_content(child['external_content'])
            elif childType == 'link_container':
                pass  # Do nothing really
            elif childType == 'video' or childType == 'image' or childType == 'quote' or childType == 'audio' or childType == 'carousel':
                pass  # print(childType, " is not currently supported")
            else:
                print("Title:", self.title)
                print(json)
                print('Unhandled content type ', childType)
                return

    def _read_external_content(self, json):

        content_type = json['content_type']

        if content_type == 'twitter':
            self.content.append(NewsItemContent({'type': 'tweet', 'url': json['url']}))
        elif content_type == 'youtube':
            self.content.append(NewsItemContent({'type': 'youtube', 'url': json['url']}))
        else:
            print('External content type', content_type, 'not currently supported')
            print(json)


class NewsItemContent:

    def __init__(self, contentJson):

        self.contentType = contentJson['type']

        if self.contentType == 'text':
            self.content = contentJson['text']
        elif self.contentType == 'title':
            self.content = contentJson['title']
        elif self.contentType == 'tweet':
            self.content = contentJson['url']


class NewsCategory:

    def __init__(self, categoryJson):
        self.name = categoryJson['name']
        self.label = categoryJson['label']
        self.main_category = categoryJson['main_category']