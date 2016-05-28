import sys
import asyncio
import telepot
from telepot.async.delegate import per_chat_id, create_open
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import NewsDataSource

class NosBot(telepot.async.helper.ChatHandler):
    def __init__(self, seed_tuple, timeout):
        super(NosBot, self).__init__(seed_tuple, timeout)

    message_with_inline_keyboard = None

    @asyncio.coroutine
    def on_chat_message(self, msg):
        #yield from self.sender.sendMessage(self._count)
        
        content_type, chat_type, chat_id = telepot.glance(msg)
        print (content_type, chat_type, chat_id)
        
        if msg['text'] == '/start':
          markup = InlineKeyboardMarkup(inline_keyboard=[
                  [InlineKeyboardButton(text='Yeah, why not?', callback_data='dailyupdates')],
                  [InlineKeyboardButton(text='No thanks!', callback_data='noupdates')]
              ])

          global message_with_inline_keyboard
          message_with_inline_keyboard = yield from self.sender.sendMessage("Hi! Thanks for coming to me. \U0001f618"
                                    "\nDo you want me to keep you updated with the news every day?"
                                    "\nIt\'ll just be a summary of the messages, don\'t worry!", reply_markup=markup)
          return
          
    @asyncio.coroutine
    def on_callback_query(self, msg):
      query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
      print ('Callback Query:', query_id, from_id, query_data)
      
      if query_data == 'dailyupdates':
        yield from self.sender.sendMessage("Got it! \U0001f60d"
                                           "\nLet\'s start with the current headlines!")
        items = news_source.cachedNews;
        for x in range(0, 3):
          item = items[x]
          yield from self.sender.sendMessage("*{}*\n{}".format(item.title, item.description), parse_mode='Markdown')
      
      elif query_data == 'noupdates':
        yield from self.sender.sendMessage("Ok, I\'ll keep my mouth shut untill you ask me! \U0001f64a")

news_source = NewsDataSource.NewsDataSource('http://s.nos.nl/extern/nieuws.json')
news_source.update_news_cache()

TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.async.DelegatorBot(TOKEN, [
    (per_chat_id(), create_open(NosBot, timeout=10)),
])

loop = asyncio.get_event_loop()
loop.create_task(bot.message_loop())
print('Listening ...')

loop.run_forever()