import lib.logger

from colorama import Fore, Back, Style
from ConfigParser import ConfigParser
from datetime import datetime
from lib.browser import Browser

# Setup debug logging
lib.logger.setupDebug();

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
        print(Fore.RED + 'FAILURE!' + Style.RESET_ALL +  ' | ' + proxyUrl)
        continue;

    totalTime = endTime - startTime
    message = Fore.GREEN + 'SUCCESS!' + Style.RESET_ALL + ' | '
    message += Fore.WHITE + Back.BLUE + (' ' + str(totalTime.total_seconds()) + 's ').ljust(12) + Style.RESET_ALL + ' | '
    message += proxyUrl
    print(message)
