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

        # Get first valid image URL and dropping weird characters/encoding
        for image in soup.select('img.SbProductBlock-image'):
            src = self.cleanString(image.get('src'))
            if src.find('http') == 0:
                self.productImageUrl = src
                break

        name = soup.select_one('p.sb_prod_name')
        self.productName = name.get_text().strip()

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
        return self.cleanString(self.productUrl)

    def getProductImageUrl(self):
        return self.cleanString(self.productImageUrl)

    def getProductName(self):
        return self.cleanString(self.productName)

    def getProductSku(self):
        return self.cleanString(self.productSku)

    def getProdutFeatureList(self):
        return self.productFeatureList

    def getProductPrice(self):
        return self.cleanString(self.productPrice)

    def getProductStars(self):
        return self.cleanString(self.productStars)

    def getProductReviews(self):
        return self.cleanString(self.productReviews)

    def cleanString(self, input):
        if input is None:
            return ''
        else:
            return input.encode('ascii', 'ignore')
