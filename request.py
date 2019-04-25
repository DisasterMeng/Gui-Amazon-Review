import requests
from fake_useragent import UserAgent

from utils import getAmazonDomain

REVIEWSURL = '{domain}/product-reviews/{asin}/ref=cm_cr_arp_d_viewopt_srt'

reviewParam = {
    'ie': 'UTF8',
    'reviewerType': 'all_reviews',
    'sortBy': 'recent',
    'pageNumber': ''
}
# 'filterByLanguage': 'en_US',


class AmazonRequests:
    def __init__(self, Country, ASIN):
        self.session = requests.Session()
        self.ASIN = ASIN
        self.Country = Country
        self.page = 1
        self.retryNum = 0
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;\
                        q=0.8,application/signed-exchange;v=b3",
            "user-agent": UserAgent().random,
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "upgrade-insecure-requests": "1"
        }

    def getURL(self):
        return REVIEWSURL.format(domain=getAmazonDomain(self.Country), asin=self.ASIN)

    def nextPage(self):
        self.page += 1

    def getPage(self):
        return self.page

    def getAmaoznData(self):
        try:
            reviewParam['pageNumber'] = str(self.getPage())
            if self.Country == 'US':
                reviewParam['filterByLanguage'] = 'en_US'
            response = self.session.get(self.getURL(), params=reviewParam, headers=self.headers, timeout=(5, 10))
            response.encoding = 'utf-8'
            if response.status_code == 200:
                return response.text
            else:
                return response.status_code
            self.retryNum = 0
        except requests.exceptions.RequestException as e:
            if self.retryNum == 2:
                print(e)
                return self.retryNum
            self.retryNum += 1
            return self.getAmaoznData()
