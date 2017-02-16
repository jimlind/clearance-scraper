#!/usr/bin/python
import util.logger
import time
import sys

from ConfigParser import ConfigParser
from lib.browser import Browser
from lib.category_page import CategoryPage
from lib.database import Database
from telegram import Bot

# Setup debug logging
util.logger.setupWarning();

config = ConfigParser()
config.read('settings.cfg')

# Allow config overrides passed as arguments
if 2 == len(sys.argv):
    config.read(sys.argv[1])

browser = Browser(
    config.getint('browser', 'courtesyTime'),
    config.get('browser', 'agent'),
    config.get('site', 'check')
)
database = Database(config.get('db', 'path') + config.get('db', 'file'))
database.updateTime()

telegramBot = Bot(token = config.get('bot', 'token'))
chatId = config.get('bot', 'chat')
url = config.get('site', 'start')
categoryCount = 0

message = config.get('scrape', 'title') + ' Started!'
telegramBot.sendMessage(chat_id=chatId, text=message)

nextCategoryAvailable = True
while nextCategoryAvailable:
    browser.setup()
    source = browser.getSource(url)
    browser.shutdown()

    categoryPage = CategoryPage(source)
    productList = categoryPage.getProductList()
    for product in productList:
        previouslyExisted = database.skuExists(product.getProductSku())
        if (previouslyExisted):
            continue

        if (product.getProductImageUrl().find('data:image') != 0):
            telegramBot.sendPhoto(chat_id = chatId, photo = product.getProductImageUrl())

        message = product.getProductUrl() + '\n\n'
        message += product.getProductName() + '\n'
        message += product.getProductPrice() + '\n'
        for feature in product.getProdutFeatureList():
            message += u' \u2022 ' + feature + '\n'

        message += product.getProductStars() + u' \u2606 ' + product.getProductReviews()
        telegramBot.sendMessage(chat_id=chatId, text=message)
        time.sleep(2)

    for product in productList:
        database.upsertItem(product.getProductSku(), product.getProductUrl())

    url = categoryPage.getNextUrl()
    if ('' == url):
        nextCategoryAvailable = False

    categoryCount += 1

database.cleanOldItems()
reportData = database.report()

message = 'Scrape Complete!\n'
message += str(reportData[0]) + ' New Products Found\n'
message += str(reportData[1]) + ' Total Products Found\n'
message += str(reportData[2]) + ' Existing Products Not Updated\n'
message += str(categoryCount) + ' Pages Scraped'
telegramBot.sendMessage(chat_id=chatId, text=message)
