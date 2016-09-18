#!/usr/bin/python
from bs4 import BeautifulSoup
from subprocess import call

import re
import time
import urlparse

class ProductBuilder:

    def parse(self, htmlString):
        soup = BeautifulSoup(htmlString, 'html.parser')
        image = soup.select('img.ProductDetailImagesBlock-carousel-image')

        href = ''
        if 1 <= len(image):
            src = image[0]['src']
            query = urlparse.urlparse(src).query
            href = urlparse.parse_qs(query).get('u')[0]
         
        returnData = {}
        returnData['href'] = href.encode('ascii', 'ignore')

        productList = []
        for cell in soup.select('table.clearancewrap td'):
            description = cell.select('p.emphasis')[0].get_text().strip()
            descriptionClean = ' '.join(description.split())

            price = cell.select('div.discount_info.textbox')[0].get_text().strip()
            priceClean = price.split().pop()
	
            returnProduct = {}
            returnProduct['d'] = descriptionClean
            returnProduct['p'] = priceClean
            productList.append(returnProduct)

        returnData['list'] = productList
        
        return returnData
