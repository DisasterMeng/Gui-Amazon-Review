import requests
from fake_useragent import UserAgent

from utils import getAmazonDomain

REVIEWSURL = '{domain}/product-reviews/{asin}?reviewerType=all_reviews&pageNumber={page}&sortBy=recent&pageSize=50'


class AmazonRequests:
    def __init__(self, Country, ASIN):
        self.ASIN = ASIN
        self.Country = Country
        self.page = 1
        self.retryNum = 0
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "user-agent": UserAgent().random,
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "upgrade-insecure-requests": "1"
        }

    def getURL(self):
        return REVIEWSURL.format(domain=getAmazonDomain(self.Country), asin=self.ASIN, page=self.page)

    def nextPage(self):
        self.page += 1

    def getPage(self):
        return self.page

    def getAmaoznData(self):
        try:
            response = requests.get(self.getURL(), headers=self.headers, timeout=(5, 10))
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
