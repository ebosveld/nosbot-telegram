import datetime

class NewsItem:

    def __init__(self, json):
        self.id = json['id']
        self.type = json['type']
        self.title = json['title']
        self.description = json['description']
        self.publish_time = datetime.datetime.strptime(json['published_at'], '%Y-%m-%dT%H:%M:%S+%f')
        self.last_modification_time = datetime.datetime.strptime(json['modified_at'], '%Y-%m-%dT%H:%M:%S+%f')

        if 'image' in json:
            self.main_image_url = json['image']['formats'][0]['url']['jpg']

        self.content = []
        self.categories = []

        for i in json['categories']:
            self.categories.append(NewsCategory(i))

        self.parseContentJsonChildren(json['content']['children'])


    def parseContentJsonChildren(self, json):

        for child in json:
            childType = child['type']
            if childType == 'text' or childType == 'title':
                self.content.append(NewsItemContent(child))
            elif childType == 'container':
                self.parseContentJsonChildren(child['children'])
            elif childType == 'external_content':
                self.analizeExternalContent(child['external_content'])
            elif childType == 'link_container':
                pass  # Do nothing really
            elif childType == 'video' or childType == 'image' or childType == 'quote' or childType == 'audio' or childType == 'carousel':
                pass  # print(childType, " is not currently supported")
            else:
                print("Title:", self.title)
                print(json)
                print('Unhandled content type ', childType)
                return

    def analizeExternalContent(self, json):

        contentType = json['content_type']

        if contentType == 'twitter':
            self.content.append(NewsItemContent({'type': 'tweet', 'url': json['url']}))
        elif contentType == 'youtube':
            self.content.append(NewsItemContent({'type': 'youtube', 'url': json['url']}))
        else:
            print('External content type', contentType, 'not currently supported')
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