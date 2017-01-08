#!/usr/bin/python
from bs4 import BeautifulSoup
from lib.product import Product

class CategoryPage:

    productList = []
    nextUrl = ''

    def __init__(self, source):
        soup = BeautifulSoup(source, 'html.parser')

        self.productList = self.extractProductList(soup)
        self.nextUrl = self.extractNextUrl(soup)

    def getProductList(self):
        return self.productList

    def getNextUrl(self):
        return self.nextUrl

    def extractProductList(self, soup):
        productList = []
        linkList = soup.find_all('a', class_='js-prod-content')
        for link in linkList:
            href = link.get('href')
            if (href.find('clearance=true') > 0):
                productList.append(Product(link))

        return productList

    def extractNextUrl(self, soup):
        link = soup.find('a', class_='js-next-page')
        if link is not None:
            href = link.get('href')
            if (href.find('http') == 0):
                return href

        return ''
