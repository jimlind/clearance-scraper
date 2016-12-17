#!/usr/bin/python
from bs4 import BeautifulSoup
import urlparse

class CategoryBuilder:

    database = None
    nextUrl = ''

    def __init__(self, database):
        self.database = database

    def parse(self, htmlString):
        soup = BeautifulSoup(htmlString, 'html.parser')
        linkList = soup.find_all('a', class_='js-prod-content')

        for link in linkList:
            href = self.extractUrl(link)
            if (href.find('clearance=true') > 0):
                self.process(href, link)

        link = soup.find('a', class_='js-next-page')
        if link is not None:
            parsedUrl = self.extractUrl(link)
            if (parsedUrl.find('http') == 0):
                self.nextUrl = parsedUrl
                return True

        return False

    def process(self, href, link):
        self.database.upsertItem(link.get('data-sku'), href)

    def getNextUrl(self):
        return self.nextUrl

    def extractUrl(self, link):
        rawHref = link.get('href')
        if (rawHref.find('http') == 0):
            return rawHref

        urlTuple = urlparse.urlparse(rawHref)
        href = urlparse.parse_qs(urlTuple.query).get('u')[0]

        return href
