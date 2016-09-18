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
        linkList = soup.find_all('a', class_='productbox')

        for link in linkList:
            href = self.extractUrl(link)
            if href.endswith('clearance=true'):
                self.process(href, link)        

        link = soup.find('a', class_='js-next-page')
        linkFound = link is not None        
        
        if linkFound:
            self.nextUrl = self.extractUrl(link)

        return linkFound

    def process(self, href, link):
        self.database.upsertItem(link.get('data-sku'), href)

    def getNextUrl(self):
        return self.nextUrl

    def extractUrl(self, link):
        urlTuple = urlparse.urlparse(link.get('href'))
        href = urlparse.parse_qs(urlTuple.query).get('u')[0]
        
        return href
