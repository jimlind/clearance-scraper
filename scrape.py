from ConfigParser import ConfigParser
from lib.browser import Browser
from lib.category_builder import CategoryBuilder
from lib.product_builder import ProductBuilder
from lib.database import Database
from telegram import Bot

config = ConfigParser()
config.read('settings.cfg')

database = Database(config.get('db', 'path') + config.get('db', 'file'))
database.updateTime()

categoryBuilder = CategoryBuilder(database)
telegramBot = Bot(token = config.get('bot', 'token'))
chatId = config.get('bot', 'chat')

url = config.get('site', 'start')
print(url)
source = Browser().getSource(url)
while categoryBuilder.parse(source):
    url = categoryBuilder.getNextUrl()
    print(url)
    source = Browser().getSource(url)

database.cleanOldItems()
reportData = database.report()

message = 'Scrape Complete!\n'
message += str(reportData[0]) + ' New Products Found\n'
message += str(reportData[1]) + ' Products Avaiable\n'
message += str(reportData[2]) + ' Products Eliglble for Delete'

if message:
    print(message)
    telegramBot.sendMessage(chat_id=chatId, text=message)

productBuilder = ProductBuilder()
for data in database.getNewUrlList():
    url = data[0]
    source = Browser().getSource(url)
    product = productBuilder.parse(source)
    if ('href' in product and product['href']):
        telegramBot.sendPhoto(chat_id=chatId, photo=product['href'])

    message = url + '\n\n'
    for item in product['list']:
        message += item['p'] + ' :: ' + item['d'] + '\n'

    if message:
        print(url)
        telegramBot.sendMessage(chat_id=chatId, text=message)
