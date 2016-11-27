import mechanize

from bs4 import BeautifulSoup
from datetime import datetime
from ConfigParser import ConfigParser
from lib.browser import Browser

def getMechanizeGoogle(agentString):
    mechBrowser = mechanize.Browser()
    mechBrowser.set_handle_robots(False)
    mechBrowser.addheaders = [('User-agent', agentString)]
    mechBrowser.open('https://www.google.com')

    mechBrowser.select_form(nr=0)
    mechBrowser.form['q'] = 'powered by glype'
    mechBrowser.submit()

    return mechBrowser

def getAnchorList(mechBrowser):
    soup = BeautifulSoup(mechBrowser.response().read(), 'html.parser')
    titleList = soup.find_all('h3')

    hrefList = [];
    for title in titleList:
        anchor = title.find('a')
        if anchor is None:
            continue
        hrefList.append(anchor.get('href'))

    return hrefList

agentString = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:48.0) Gecko/20100101 Firefox/48.0'
mechBrowser = getMechanizeGoogle(agentString)

totalPages = 6
googleResultList = []
for i in range(totalPages):
    googleResultList = googleResultList + getAnchorList(mechBrowser)
    if i < (totalPages - 1):
        request = mechBrowser.click_link(text='Next')
        mechBrowser.open(request)
mechBrowser.close()
print('Found ' + str(len(googleResultList)) + ' results. We are going to test them now.')

config = ConfigParser()
config.read('settings.cfg')
check = config.get('site', 'check')
url = config.get('site', 'start')

for googleResult in googleResultList:
    proxyUrl = googleResult[:googleResult.rfind('/')] + '/index.php'
    browser = Browser([proxyUrl], check)
    browser.setup()
    startTime = datetime.now()
    source = browser.getSourceOrFalse(url)
    endTime = datetime.now()
    browser.shutdown()

    if (False == source):
        continue;

    totalTime = endTime - startTime
    totalSecondsString = str(totalTime.total_seconds())
    print('It took ' + totalSecondsString + ' seconds to successfully use ' + proxyUrl)
