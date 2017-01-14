#!/usr/bin/python
import util.logger

from ConfigParser import ConfigParser
from lib.browser import Browser
from lib.category_page import CategoryPage
from lib.database import Database
from telegram import Bot


# Setup debug logging
util.logger.setupWarning();

config = ConfigParser()
config.read('settings.cfg')

browser = Browser(config.get('site', 'check'))
database = Database(config.get('db', 'path') + config.get('db', 'file'))
database.updateTime()

telegramBot = Bot(token = config.get('bot', 'token'))
chatId = config.get('bot', 'chat')
url = config.get('site', 'start')

nextCategoryAvailable = True
while nextCategoryAvailable:
    browser.setup()
    source = browser.getSource(url)
    browser.shutdown()

    categoryPage = CategoryPage(source)
    for product in categoryPage.getProductList():
        previouslyExisted = database.skuExists(product.getProductSku())
        database.upsertItem(product.getProductSku(), product.getProductUrl())
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

    url = categoryPage.getNextUrl()
    if ('' == url):
        nextCategoryAvailable = False

# database.cleanOldItems()
reportData = database.report()

message = 'Scrape Complete!\n'
message += str(reportData[0]) + ' New Products Found\n'
message += str(reportData[1]) + ' Products Avaiable\n'
message += str(reportData[2]) + ' Products Eliglble for Delete'
telegramBot.sendMessage(chat_id=chatId, text=message)
