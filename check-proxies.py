from datetime import datetime
from ConfigParser import ConfigParser
from lib.browser import Browser

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
        print('          >>> FAILURE! Unable to use this proxy at this time.')
        continue;

    totalTime = endTime - startTime
    totalSecondsString = str(totalTime.total_seconds())
    print('          >>> SUCCESS! It took ' + totalSecondsString + ' seconds on this proxy.')
