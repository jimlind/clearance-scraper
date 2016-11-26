from datetime import datetime
from ConfigParser import ConfigParser
from lib.browser import Browser
from lib.category_builder import CategoryBuilder
from lib.product_builder import ProductBuilder
from lib.database import Database
from telegram import Bot

config = ConfigParser()
config.read('settings.cfg')

check = config.get('site', 'check')
url = config.get('site', 'start')
print('Store URL === ' + url)

rawProxyList = config.get('proxy', 'list').split()
for rawProxy in rawProxyList:
    proxyUrl = rawProxy.strip()
    print('Proxy URL === ' + proxyUrl)
    browser = Browser([proxyUrl], check)
    browser.setup()
    startTime = datetime.now()
    source = browser.getSourceOrFalse(url)
    endTime = datetime.now()
    browser.shutdown()

    if (False == source):
        print('   >>> FAILURE! Unable to use this proxy at this time.')
        continue;

    totalTime = endTime - startTime
    totalSecondsString = str(totalTime.total_seconds())
    print('   >>> SUCCESS! It took ' + totalSecondsString + ' seconds on this proxy.')

    # proxyList = [rawProxy.strip()]
    # print(proxyList)
#
# check = config.get('site', 'check')
# browser = Browser(proxyList, check)
#
# nextCategoryAvailable = True
# url = config.get('site', 'start')
# while nextCategoryAvailable:
#     browser.setup()
#     source = browser.getSource(url)
#     browser.shutdown()
#
#     nextCategoryAvailable = categoryBuilder.parse(source)
#     url = categoryBuilder.getNextUrl()
#
# database.cleanOldItems()
# reportData = database.report()
