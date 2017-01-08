#!/usr/bin/python
from bs4 import BeautifulSoup
from subprocess import call

import re
import time
import urlparse

class Product:

    productUrl = ''
    productImageUrl = ''
    productName = ''
    productSku = ''
    productFeatureList = []
    productPrice = ''
    productStars = ''
    productReviews = ''

    def __init__(self, soup):
        self.productUrl = soup.get('href')
        self.productSku = soup.get('data-sku')

        # Get image URL and drop any weird characters/encoding
        image = soup.select_one('img.SbProductBlock-image')
        self.productImageUrl = image.get('src').encode('ascii', 'ignore')

        name = soup.select_one('div.sb_names')
        self.productName = name.get('title')

        # Get price make sure it looks like real money
        price = soup.find('span', attrs={'data-price': True})
        priceFloat = float(price.get('data-price'))
        self.productPrice = '$' + format(priceFloat, '.2f')

        featureList = []
        for feature in soup.select('li.sb_prod_feature_item'):
            featureList.append(feature.get_text().strip())
        self.productFeatureList = featureList

        stars = soup.select_one('span.stars_wrap')
        if stars is not None:
            self.productStars = stars.get('aria-label')

        # Strip some special symbols really fast
        review = soup.select_one('div.reviewbox')
        if review is not None:
            reviewText = review.get_text().replace('(', '').replace(')', '')
            self.productReviews = ' '.join(reviewText.split())

    def getProductUrl(self):
        return self.productUrl

    def getProductImageUrl(self):
        return self.productImageUrl

    def getProductName(self):
        return self.productName

    def getProductSku(self):
        return self.productSku

    def getProdutFeatureList(self):
        return self.productFeatureList

    def getProductPrice(self):
        return self.productPrice

    def getProductStars(self):
        return self.productStars

    def getProductReviews(self):
        return self.productReviews
