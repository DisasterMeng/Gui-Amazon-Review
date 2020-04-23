import requests
from urllib.parse import urlencode
from fake_useragent import UserAgent

from utils import getAmazonDomain, amazon_headers

REVIEWSURL = '{domain}/product-reviews/{asin}/ref=cm_cr_arp_d_viewopt_srt'

reviewParam = {
    'ie': 'UTF8',
    'reviewerType': 'all_reviews',
    'sortBy': 'recent',
    'pageNumber': ''
}


class AmazonRequests:
    def __init__(self, country, asin, session, proxies):
        self.session = session if session else requests.session()
        self.proxies = proxies
        self.ASIN = asin
        self.Country = country
        self.page = 1
        self.retryNum = 0
        self.referer = getAmazonDomain(self.Country)
        self.headers = amazon_headers.copy()
        self.headers['user-agent'] = UserAgent().random

    def getURL(self):
        return REVIEWSURL.format(domain=getAmazonDomain(self.Country), asin=self.ASIN)

    def nextPage(self):
        self.page += 1

    def getPage(self):
        return self.page

    def getAmaoznData(self, is_lang=False):
        try:
            reviewParam['pageNumber'] = str(self.getPage())
            if is_lang and self.Country == 'US':
                reviewParam['filterByLanguage'] = 'en_US'
            self.headers['referer'] = self.referer
            response = self.session.get(self.getURL(), params=reviewParam, headers=self.headers, proxies=self.proxies, timeout=(5, 10))
            response.encoding = 'utf-8'
            self.referer = '%s?%s' % (self.getURL(), urlencode(reviewParam))
            if response.status_code == 200:
                return response.text
            else:
                return response.status_code
        except requests.exceptions.RequestException as e:
            if self.retryNum == 2:
                print(e)
                return self.retryNum
            self.retryNum += 1
            return self.getAmaoznData()
