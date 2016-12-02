import lib.logger

from ConfigParser import ConfigParser
from lib.browser import Browser
from lib.category_builder import CategoryBuilder
from lib.product_builder import ProductBuilder
from lib.database import Database
from telegram import Bot

# Setup debug logging
lib.logger.setupWarning();

config = ConfigParser()
config.read('settings.cfg')

database = Database(config.get('db', 'path') + config.get('db', 'file'))
database.updateTime()

categoryBuilder = CategoryBuilder(database)
telegramBot = Bot(token = config.get('bot', 'token'))
chatId = config.get('bot', 'chat')

rawProxyList = config.get('proxy', 'list').split()
proxyList = []
for rawProxy in rawProxyList:
    proxyList.append(rawProxy.strip())
check = config.get('site', 'check')
browser = Browser(proxyList, check)

nextCategoryAvailable = True
url = config.get('site', 'start')
while nextCategoryAvailable:
    browser.setup()
    source = browser.getSource(url)
    browser.shutdown()

    nextCategoryAvailable = categoryBuilder.parse(source)
    url = categoryBuilder.getNextUrl()

database.cleanOldItems()
reportData = database.report()

message = 'Scrape Complete!\n'
message += str(reportData[0]) + ' New Products Found\n'
message += str(reportData[1]) + ' Products Avaiable\n'
message += str(reportData[2]) + ' Products Eliglble for Delete'
telegramBot.sendMessage(chat_id=chatId, text=message)

productBuilder = ProductBuilder()
for data in database.getNewUrlList():
    url = data[0]

    browser.setup()
    source = browser.getSource(url)
    browser.shutdown()

    product = productBuilder.parse(source)
    if ('href' in product and product['href']):
        telegramBot.sendPhoto(chat_id=chatId, photo=product['href'])

    message = url + '\n\n'
    for item in product['list']:
        message += item['p'] + ' :: ' + item['d'] + '\n'

    if message:
        telegramBot.sendMessage(chat_id=chatId, text=message)
