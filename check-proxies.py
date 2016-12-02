import util.display
import util.logger

from ConfigParser import ConfigParser
from datetime import datetime
from lib.browser import Browser

# Setup debug logging
util.logger.setupDebug();

config = ConfigParser()
config.read('settings.cfg')

check = config.get('site', 'check')
url = config.get('site', 'start')

rawProxyList = config.get('proxy', 'list').split()
for rawProxy in rawProxyList:
    proxyUrl = rawProxy.strip()
    browser = Browser([proxyUrl], check)
    browser.setup()
    startTime = datetime.now()
    source = browser.getSourceOrFalse(url)
    endTime = datetime.now()
    browser.shutdown()

    if (False == source):
        util.display.failure('', proxyUrl)
        continue;

    seconds = (endTime - startTime).total_seconds()
    util.display.success(str(seconds), proxyUrl)
